import copy
import logging
import math
import numpy as np
import os
import pandas as pd
import datetime
import time

from auger_ml.FSClient import FSClient
from auger_ml.data_source.data_source_api_pandas import DataSourceAPIPandas, load_each_df_from_bin_file
from auger_ml.data_splitters.XYNumpyDataPrep import XYNumpyDataPrep
from auger_ml.Utils import remove_dups_from_list, get_uid, get_uid4, convert_to_date, merge_dicts


class ModelExporter(object):
    def __init__(self, options):
        self.options = options

    def load_model(self, model_path):
        from auger_ml.preprocessors.space import ppspace_is_timeseries_model

        model = FSClient().loadObjectFromFile(os.path.join(model_path, "model.pkl.gz"))

        options = FSClient().readJSONFile(os.path.join(model_path, "options.json"))
        timeseries_model = options.get('timeSeriesFeatures') and ppspace_is_timeseries_model(options.get('algorithm_name'))

        return model, timeseries_model

    def preprocess_target(self, model_path, data_path=None, records=None, features=None):

        ds = DataSourceAPIPandas.create_dataframe(data_path, records, features)

        return self.preprocess_target_ds(model_path, ds)

    def preprocess_target_ds(self, model_path, ds):
        import numpy as np

        options = FSClient().readJSONFile(os.path.join(model_path, "options.json"))
        target_categoricals = FSClient().readJSONFile(os.path.join(model_path, "target_categoricals.json"))
        y_true =  None

        if not options.get('targetFeature') or not options.get('targetFeature') in ds.columns:
            return y_true, target_categoricals

        if options.get('timeSeriesFeatures'):
            y_true = np.ravel(ds.df[options.get('targetFeature')].astype(np.float64, copy=False), order='C')
        else:
            if target_categoricals and options.get('targetFeature') in target_categoricals:
                ds.convertToCategorical(options.get('targetFeature'), is_target=True,
                    categories=target_categoricals.get(options.get('targetFeature')).get('categories'))

            y_true = np.ravel(ds.df[options.get('targetFeature')], order='C')

        return y_true, target_categoricals

    def preprocess_data(self, model_path, data_path=None, records=None, features=None, predict_value_num=None):
        from auger_ml.AugerMLPreprocessors import AugerMLPreprocessors
        from auger_ml.preprocessors.space import ppspace_is_timeseries_model, pspace_get_fold_group_names

        options = FSClient().readJSONFile(os.path.join(model_path, "options.json"))
        fold_group_props = FSClient().readJSONFile(os.path.join(model_path, options['fold_group'], "data_preprocessed.props.json"))

        if fold_group_props and 'featureColumns' in fold_group_props:
            train_features = copy.deepcopy(fold_group_props['featureColumns'])
        else:
            train_features = copy.deepcopy(options['featureColumns'])

        options['featureColumns'] = options.get('originalFeatureColumns')
        data_features = options['featureColumns'][:]
        if options.get('timeSeriesFeatures'):
            data_features.extend(options.get('timeSeriesFeatures'))
            data_features.append(options.get('targetFeature'))

        data_features = remove_dups_from_list(data_features)

        if features is None:
            features = data_features

        ds = DataSourceAPIPandas.create_dataframe(data_path, records, features)

        if set(data_features).issubset(set(ds.columns)):
            if options.get('targetFeature') in ds.columns and not options.get('targetFeature') in data_features:
                data_features.append(options.get('targetFeature'))

            ds.df = ds.df[data_features]
        else:
            raise Exception("Prediction data missing columns:%s"%(set(data_features)-set(ds.columns)))

        transforms = FSClient().readJSONFile(os.path.join(model_path, "transformations.json"))
        ds.transform(transforms, cache_to_file=False)

        target_categoricals = FSClient().readJSONFile(os.path.join(model_path, "target_categoricals.json"))

        X_test, Y_test = None, None
        if options.get('timeSeriesFeatures'):

            if predict_value_num is not None:
                if predict_value_num == len(ds.df):
                    return None, None, None

                ds.df = ds.df.iloc[:(predict_value_num + 1)]  # truncate dataset

            pp = AugerMLPreprocessors(options)
            pp.transform_predicted_data(ds, model_path, target_categoricals)

            X_test, Y_test = XYNumpyDataPrep(options).split_predict_timeseries(ds.df, train_features)

        else:
            X_test = {}
            if options.get('ensemble', False):
                fold_groups = pspace_get_fold_group_names(options.get('timeSeriesFeatures'))
                for fold_group in fold_groups:
                    options['fold_group'] = fold_group

                    ds2 = DataSourceAPIPandas(options)
                    ds2.df = ds.df.copy()

                    pp = AugerMLPreprocessors(options)
                    pp.transform_predicted_data(ds2, model_path, target_categoricals)
                    fold_group_props_1 = FSClient().readJSONFile(os.path.join(model_path, fold_group, "data_preprocessed.props.json"))

                    fold_group_features = train_features
                    if fold_group_props_1 and 'featureColumns' in fold_group_props_1:
                        fold_group_features = fold_group_props_1['featureColumns']

                    X_test[fold_group], Y_test = XYNumpyDataPrep(options).split_predict(ds2.df, fold_group_features)
            else:
                pp = AugerMLPreprocessors(options)
                pp.transform_predicted_data(ds, model_path, target_categoricals)
                X_test, Y_test = XYNumpyDataPrep(options).split_predict(ds.df, train_features)

        return X_test, Y_test, target_categoricals

    def check_model_path(self):
        from auger_ml.core.AugerML import AugerML

        if not self.options.get('model_path'):
            params = copy.deepcopy(self.options)
            params = AugerML.update_task_params(params)
            self.options['model_path'] = os.path.join(params['augerInfo']['modelsPath'], params['augerInfo']['pipeline_id'])
            # if 'augerInfo' in self.options:
            #     del self.options['augerInfo']

        return self

    def predict_by_model(self, model_path, path_to_predict=None, records=None,
        features=None, threshold=None, predict_value_num=None, json_result=False, count_in_result=False):
        from auger_ml.preprocessors.space import ppspace_is_timeseries_model

        X_test, Y_test, target_categoricals = self.preprocess_data(model_path,
            data_path=path_to_predict, records=records, features=features, predict_value_num=predict_value_num)

        # print("Start loading model: %s"%datetime.datetime.utcnow())
        model, timeseries_model = self.load_model(model_path)
        # print("End loading model: %s"%datetime.datetime.utcnow())

        if X_test is None:
            return None

        options = FSClient().readJSONFile(os.path.join(model_path, "options.json"))

        ds = DataSourceAPIPandas({'data_path': path_to_predict})
        if options.get('timeSeriesFeatures'):
            if ppspace_is_timeseries_model(options.get('algorithm_name')):
                results = model.predict((X_test, Y_test, False))[-1:]
            else:
                results = model.predict(X_test.iloc[-1:])

            ds.df = pd.DataFrame({
                options['targetFeature']: results,
                options['timeSeriesFeatures'][0]: X_test.index[-1:]
            })
        else:
            results = None
            results_proba = None
            proba_classes = None
            proba_classes_orig = None
            try:
                if threshold:
                    if hasattr(model, 'predict_proba') and callable(getattr(model, 'predict_proba')):
                        try:
                            results_proba = model.predict_proba(X_test)
                        except AttributeError as e:
                            logging.info("predict_proba is property, try _predict_proba")
                            results_proba = model._predict_proba(X_test)

                    elif hasattr(model, 'decision_function'):
                        results_proba = model.decision_function(X_test)

                    if results_proba is not None:
                        proba_classes = list(model.classes_)
                        if options['targetFeature'] in target_categoricals:
                            proba_classes_orig = list(DataSourceAPIPandas.revertCategories(proba_classes,
                                                      target_categoricals[options['targetFeature']]['categories']))

                        results = self._calculate_proba_target(results_proba,
                            proba_classes,
                            proba_classes_orig,
                            threshold,
                            options.get('minority_target_class'))
            except:
                logging.exception("predict_proba failed.")

            if results is None:
                results = model.predict(X_test)

            try:
                results = list(results)
            except Exception as e:
                #print("INFO: Prediction result with type: %s convert to list failed: %s"%(type(results), str(e)))
                results = [results]

            if options['targetFeature'] in target_categoricals:
                results = DataSourceAPIPandas.revertCategories(results,
                                              target_categoricals[options['targetFeature']]['categories'])
                if proba_classes_orig is not None:
                    proba_classes = proba_classes_orig

            if path_to_predict:
                ds.load(use_cache=False)
            else:
                ds.load_records(records, features=features, use_cache=False)

            #drop target
            if options['targetFeature'] in ds.columns:
                ds.drop([options['targetFeature']])

            try:
                results = list(results)
            except Exception as e:
                #print("INFO: Prediction result with type: %s convert to list failed: %s"%(type(results), str(e)))
                results = [results]

            ds.df[options['targetFeature']] = results
            if results_proba is not None:
                for idx, name in enumerate(proba_classes):
                    ds.df['proba_'+str(name)] = list(results_proba[:,idx])

                #ds.df = self._format_proba_predictions(ds.df)

        # Ids for each row of prediction (predcition row's ids)
        prediction_ids = []
        for i in range(0,ds.count()):
            prediction_ids.append(get_uid4())

        ds.df.insert(loc=0, column='prediction_id', value=prediction_ids)

        # Id for whole prediction (can contains many rows)
        uid_prediction = self.options.get('prediction_id', get_uid())

        #print(ds.df)
        if options.get('support_review_model', False):
            file_name = str(datetime.date.today()) + '_' + uid_prediction + "_results.pkl.gz"
            ds.saveToBinFile(os.path.join(model_path, "predictions", file_name))

        if path_to_predict and not json_result:
            parent_path = FSClient().getParentFolder(path_to_predict)
            file_name = os.path.basename(path_to_predict)
            predict_path = os.path.join( parent_path, "predictions",
                os.path.splitext(file_name)[0] + "_%s_%s_predicted.csv"%(uid_prediction, options.get('uid')))
            ds.saveToCsvFile(predict_path, compression=None)
            #print(predict_path)

            if count_in_result:
                return {'result_path': predict_path, 'count': ds.count()}
            else:
                return predict_path
        else:
            if json_result:
                return ds.df.to_json(orient='split', index=False)

            return ds.df

    def _calculate_proba_target(self, results_proba, proba_classes, proba_classes_orig, threshold, minority_target_class=None):
        import json
        results = []

        if type(threshold) == str:
            try:
                threshold = float(threshold)
            except:
                try:
                    threshold = json.loads(threshold)
                except Exception as e:
                    raise Exception("Threshold '%s' should be float or hash with target classes. Error: %s"%(threshold, str(e)))

        if type(threshold) != dict and minority_target_class is not None:
            threshold = {minority_target_class:threshold}

        print("Prediction threshold: %s, %s"%(threshold, proba_classes_orig))
        #print(results_proba)
        if type(threshold) == dict:
            mapped_threshold = {}
            if not proba_classes_orig:
                proba_classes_orig = proba_classes

            for name, value in threshold.items():
                idx_class = None
                for idx, item in enumerate(proba_classes_orig):
                    if item == name:
                        idx_class = idx
                        break

                if idx_class is None:
                    raise Exception("Unknown target class in threshold: %s, %s"%(name, proba_classes_orig))

                mapped_threshold[idx_class] = value

            for item in results_proba:
                proba_idx = None
                for idx, value in mapped_threshold.items():
                    if item[idx] >= value:
                        proba_idx = idx
                        break

                if proba_idx is None:
                    proba_idx = 0
                    for idx, value in enumerate(item):
                        if idx not in mapped_threshold:
                            proba_idx = idx
                            break

                results.append(proba_classes[proba_idx])
        else:
            #TODO: support multiclass classification
            for item in results_proba:
                max_proba_idx = 0
                for idx, prob in enumerate(item):
                    if prob > item[max_proba_idx]:
                        max_proba_idx = idx

                if item[max_proba_idx] < threshold:
                    if max_proba_idx > 0:
                        max_proba_idx = 0
                    else:
                        max_proba_idx = 1

                results.append(proba_classes[max_proba_idx])

        return results

    def _format_proba_predictions(self, predictions):
        predictions_no_proba = predictions[predictions.columns.drop(
            list(predictions.filter(regex='proba_'))
        )]
        predictions_proba = predictions.filter(regex='proba_').reset_index()
        predictions = predictions_no_proba.reset_index().iloc[:, list((0, -1))]

        if not predictions_proba.empty:
            predictions = pd.merge(predictions, predictions_proba, on='index')

        predictions.drop(['index'], inplace=True, axis=1)

        return predictions

    def predict_by_model_ts_recursive(self, model_path, path_to_predict=None, records=None, features=None,
                                      start_prediction_num=None):
        options = FSClient().readJSONFile(os.path.join(model_path, "options.json"))
        targetFeature = options['targetFeature']

        i = start_prediction_num
        result = []
        while True:
            res = self.predict_by_model(model_path, path_to_predict, records, features, predict_value_num=i)
            if res is None:
                break

            if path_to_predict is not None:
                ds = DataSourceAPIPandas({'data_path': res})
                ds.load(features = [targetFeature], use_cache = False)
                res = ds.df
                #res = pd.read_csv(res, encoding='utf-8', escapechar='\\', usecols=[targetFeature])

            #assert len(res) == 1
            result.append(res[targetFeature][0])
            i += 1

        return result

    def score_by_model(self, model_path, predict_path=None, test_path=None,
            records=None, features=None, test_records=None, test_features=None,
            start_prediction_num=20, predictions=None):
        from auger_ml.Utils import calculate_scores

        res = {}
        options = FSClient().readJSONFile(os.path.join(model_path, "options.json"))
        y_pred = None

        if options.get('timeSeriesFeatures'):
            y_pred = self.predict_by_model_ts_recursive(model_path,
                path_to_predict=predict_path, records=records, features=features, start_prediction_num=start_prediction_num)
        else:
            if predictions is None:
                predictions = self.predict_by_model(model_path, path_to_predict=predict_path,
                    records=records, features=features)

            if predict_path:
                y_pred, target_categoricals = self.preprocess_target(model_path, data_path=predictions)
            else:
                y_pred, target_categoricals = self.preprocess_target(model_path, records=predictions, features=[options.get('targetFeature')])

            #TODO: support proba scores and threshold

        if test_path is None and test_records is None:
            test_path = predict_path

        y_true, target_categoricals = self.preprocess_target(model_path, data_path=test_path,
            records=test_records, features=test_features)

        if test_path == predict_path:
            y_true = y_true[:len(y_pred)]

        res['all_scores'] = calculate_scores(options, y_test=y_true, y_pred=y_pred, raise_main_score=False)

        return res

    def score_actuals(self, model_path, actuals_path = None, actual_records=None, actuals_ds=None):
        from auger_ml.Utils import calculate_scores

        options = FSClient().readJSONFile(os.path.join(model_path, "options.json"))
        target_feature = options.get('targetFeature')

        # if there are hashes in actual_records or file try to load all columns
        features = ['prediction_id', target_feature, 'actual']

        # if there are lists with value couples in actual_records use only two columns
        if actual_records and type(actual_records[0]) == list and len(actual_records[0]) == 2:
            features = ['prediction_id', 'actual']

        ds_actuals = actuals_ds or DataSourceAPIPandas.create_dataframe(actuals_path, actual_records, features)
        # print(ds_actuals.df.drop(['prediction_id'], axis=1))

        if target_feature in ds_actuals.columns and ds_actuals.df[target_feature].any():
            ds_actuals.df.rename(columns={target_feature: 'auger_actual'}, inplace=True)
            ds_actuals.df.drop(columns=['actual'], errors='ignore', inplace=True)
        elif 'actual' in ds_actuals.columns and ds_actuals.df['actual'].any():
            ds_actuals.df.rename(columns={'actual': 'auger_actual'}, inplace=True)
            ds_actuals.df.drop(columns=[target_feature], errors='ignore', inplace=True)

        ds_actuals.df.set_index('prediction_id', inplace=True)
        actuals_count = ds_actuals.count()
        predictions_path = os.path.join(model_path, "predictions/*_results.pkl.gz")

        all_files = FSClient().listFolder(predictions_path, wild=True, removeFolderName=True, meta_info=True)
        all_files.sort(key=lambda f: f['last_modified'], reverse=True)

        if len(all_files) == 0:
            raise Exception('there is no prediction results for this model in ' + predictions_path)

        origin_dtypes = []
        origin_columns = []

        for (file, df_prediction_results) in load_each_df_from_bin_file(model_path, all_files):
            origin_dtypes = df_prediction_results.df.dtypes
            origin_columns = df_prediction_results.df.columns

            underscore_split = file['path'].split('_')

            if len(underscore_split) == 3: # date_group-id_suffix (new file name with date)
                prediction_group_id = underscore_split[1]
            else: # group-id_suffix (old file name without date)
                prediction_group_id = underscore_split[0]

            df_prediction_results.df['prediction_group_id'] = prediction_group_id
            df_prediction_results.df.set_index('prediction_id', inplace=True)
            ds_actuals.df = ds_actuals.df.combine_first(df_prediction_results.df)

            match_count = ds_actuals.df.count()[target_feature]
            if actuals_count == match_count:
                break

        ds_actuals.df.reset_index(inplace=True)
        ds_actuals.dropna(columns=[target_feature, 'auger_actual'])

        # combine_first changes orginal non float64 types to float64 when NaN values appear during merging tables
        # Good explanations https://stackoverflow.com/a/15353297/898680
        # Fix: store original datypes and force them after merging
        for col in origin_columns:
            if col != 'prediction_id':
                ds_actuals.df[col] = ds_actuals.df[col].astype(origin_dtypes[col], copy=False)

        ds_actuals.df['auger_actual'] = ds_actuals.df['auger_actual'].astype(
            origin_dtypes[target_feature], copy=False
        )

        ds_true = DataSourceAPIPandas({})
        ds_true.df = ds_actuals.df[['auger_actual']].rename(columns={'auger_actual':target_feature})

        y_pred, _ = self.preprocess_target_ds(model_path, ds_actuals)
        y_true, _ = self.preprocess_target_ds(model_path, ds_true)

        score = calculate_scores(options, y_test=y_true, y_pred=y_pred)

        if not actuals_ds:
            ds_actuals.drop(target_feature)
            ds_actuals.df = ds_actuals.df.rename(columns={'auger_actual':target_feature})

            uid_actuals = self.options.get('actuals_id', get_uid())
            file_name = str(datetime.date.today()) + '_' + uid_actuals + "_actuals.pkl.gz"
            ds_actuals.saveToBinFile(os.path.join(model_path, "predictions", file_name))

        return score

    def build_review_data(self, model_path, data_path=None):
        options = FSClient().readJSONFile(os.path.join(model_path, "options.json"))
        if not data_path:
            data_path = options['data_path']

        review_data_path = os.path.splitext(data_path)[0] + "_review_%s.pkl.gz"%(get_uid())

        ds_train = DataSourceAPIPandas.create_dataframe(data_path)

        all_files = FSClient().listFolder(os.path.join(model_path, "predictions/*_actuals.pkl.gz"),
            wild=True, removeFolderName=True, meta_info=True)
        all_files.sort(
            key=lambda f: f['last_modified'],
            reverse=True
        )

        for (file, ds_actuals) in load_each_df_from_bin_file(model_path, all_files):
            ds_actuals.drop(['prediction_id'])

            ds_train.df = pd.concat([ds_train.df, ds_actuals.df], ignore_index=True)
            ds_train.drop_duplicates()

        ds_train.saveToBinFile(review_data_path)

        return review_data_path
