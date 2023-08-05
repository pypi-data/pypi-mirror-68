# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from nwae.ml.modelhelper.ModelHelper import ModelHelper
from nwae.ml.trainer.TextTrainer import TextTrainer
import nwae.ml.TrainingDataModel as tdm
import nwae.utils.Log as log
from inspect import currentframe, getframeinfo
import nwae.math.NumpyUtil as npUtil
from nwae.ml.config.Config import Config
import nwae.utils.Profiling as prf
from nwae.utils.UnitTest import ResultObj, UnitTestParams
from nwae.lang.preprocessing.BasicPreprocessor import BasicPreprocessor


class UnitTestMetricSpaceModel:

    IDENTIFIER_STRING = 'demo_ut1'

    DATA_X = np.array(
        [
            # 무리 0
            [1, 2, 1, 1, 0, 0],
            [2, 1, 2, 1, 0, 0],
            [1, 1, 1, 1, 0, 0],
            # 무리 1
            [0, 1, 2, 1, 0, 0],
            [0, 2, 2, 2, 0, 0],
            [0, 2, 1, 2, 0, 0],
            # 무리 2
            [0, 0, 0, 1, 2, 3],
            [0, 1, 0, 2, 1, 2],
            [0, 1, 0, 1, 1, 2],
            # 무리 3 (mix)
            [1, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 2],
            [2, 0, 0, 0, 0, 1],
            [0, 1, 1, 1, 1, 0],
            [0, 1, 2, 1, 1, 0],
            [0, 1, 1, 2, 1, 0]
        ]
    )
    DATA_TEXTS = [
        # 0
        ['하나', '두', '두', '셋', '넷'],
        ['하나', '하나', '두', '셋', '셋', '넷'],
        ['하나', '두', '셋', '넷'],
        # 1
        ['두', '셋', '셋', '넷'],
        ['두', '두', '셋', '셋', '넷', '넷'],
        ['두', '두', '셋', '넷', '넷'],
        # 2
        ['넷', '다섯', '다섯', '여섯', '여섯', '여섯'],
        ['두', '넷', '넷', '다섯', '다섯', '여섯', '여섯'],
        ['두', '넷', '다섯', '여섯', '여섯'],
        # 3
        ['하나', '여섯'],
        ['하나', '여섯', '여섯'],
        ['하나', '하나', '여섯'],
        ['두', '셋', '넷', '다섯'],
        ['두', '셋', '셋', '넷', '다섯'],
        ['두', '셋', '넷', '넷', '다섯']
    ]
    DATA_Y = np.array(
        [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 3, 3, 3]
    )
    DATA_X_NAME = np.array(['하나', '두', '셋', '넷', '다섯', '여섯'])

    #
    # To test against trained models
    # Need to add one more dimension at the end for "_unk"
    #
    DATA_TEST_X = np.array(
        [
            # 무리 0
            [1.2, 2.0, 1.1, 1.0, 0, 0, 0],
            [2.1, 1.0, 2.4, 1.0, 0, 0, 0],
            [1.5, 1.0, 1.3, 1.0, 0, 0, 0],
            # 무리 1
            [0, 1.1, 2.5, 1.5, 0, 0, 0],
            [0, 2.2, 2.6, 2.4, 0, 0, 0],
            [0, 2.3, 1.7, 2.1, 0, 0, 0],
            # 무리 2
            [0, 0.0, 0, 1.6, 2.1, 3.5, 0],
            [0, 1.4, 0, 2.7, 1.2, 2.4, 0],
            [0, 1.1, 0, 1.3, 1.3, 2.1, 0],
            # 무리 3
            [1.1, 0.0, 0.0, 0.0, 0.0, 1.5, 0],
            [0.0, 1.4, 0.9, 1.7, 1.2, 0.0, 0]
        ]
    )
    DATA_TEST_X_NAME = np.array(['하나', '두', '셋', '넷', '다섯', '여섯', BasicPreprocessor.W_UNK])

    #
    # Layers Design
    #
    NEURAL_NETWORK_LAYERS = [
        {
            'units': 128,
            'activation': 'relu',
            'input_shape': (DATA_X.shape[1],)
        },
        {
            # 4 unique classes
            'units': 4,
            'activation': 'softmax'
        }
    ]

    def __init__(
            self,
            ut_params,
            model_name
    ):
        self.ut_params = ut_params
        if self.ut_params is None:
            # We only do this for convenience, so that we have access to the Class methods in UI
            self.ut_params = UnitTestParams()
        self.identifier_string = UnitTestMetricSpaceModel.IDENTIFIER_STRING
        self.model_name = model_name

        self.x_expected = UnitTestMetricSpaceModel.DATA_X
        self.texts = UnitTestMetricSpaceModel.DATA_TEXTS

        self.y = UnitTestMetricSpaceModel.DATA_Y
        self.x_name = UnitTestMetricSpaceModel.DATA_X_NAME
        #
        # Finally we have our text data in the desired format
        #
        y_list = self.y.tolist()
        y_list = list(y_list)
        self.tdm_obj = tdm.TrainingDataModel.unify_word_features_for_text_data(
            label_id       = y_list.copy(),
            label_name     = y_list.copy(),
            sentences_list = self.texts,
            keywords_remove_quartile = 0
        )

        self.x_friendly = self.tdm_obj.get_print_friendly_x()
        log.Log.debug(
            str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
            + ': x = ' + str(self.tdm_obj.get_x())
        )
        for k in self.x_friendly.keys():
            log.Log.debugdebug(self.x_friendly[k])
        log.Log.debug(
            str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
            + ': x_name = ' + str(self.tdm_obj.get_x_name())
        )
        log.Log.debug(
            str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
            + ': y = ' + str(self.tdm_obj.get_y())
        )
        return

    def unit_test_train(
            self,
            model_params = None
    ):
        trainer_obj = TextTrainer(
            identifier_string = self.identifier_string,
            model_name        = self.model_name,
            model_params      = model_params,
            dir_path_model    = self.ut_params.dirpath_model,
            training_data     = self.tdm_obj
        )

        trainer_obj.train(
            write_training_data_to_storage = True
        )

        # How to make sure order is the same output from TextCluster in unit tests?
        x_name_expected = ['넷' '두' '셋' '여섯' '다섯' '하나']

        sentence_matrix_expected = np.array([
            [0.37796447, 0.75592895, 0.37796447, 0., 0., 0.37796447],
            [0.31622777, 0.31622777, 0.63245553, 0., 0., 0.63245553],
            [0.5, 0.5, 0.5, 0., 0., 0.5],
            [0.40824829, 0.40824829, 0.81649658, 0., 0., 0.],
            [0.57735027, 0.57735027, 0.57735027, 0., 0., 0.],
            [0.66666667, 0.66666667, 0.33333333, 0., 0., 0.],
            [0.26726124, 0., 0., 0.80178373, 0.53452248, 0.],
            [0.5547002, 0.2773501, 0., 0.5547002, 0.5547002, 0.],
            [0.37796447, 0.37796447, 0., 0.75592895, 0.37796447, 0.]
        ])
        for i in range(0, sentence_matrix_expected.shape[0], 1):
            v = sentence_matrix_expected[i]
            ss = np.sum(np.multiply(v, v)) ** 0.5
            log.Log.debugdebug(v)
            log.Log.debugdebug(ss)

        agg_by_labels_expected = np.array([
            [1.19419224, 1.57215671, 1.51042001, 0., 0., 1.51042001],
            [1.65226523, 1.65226523, 1.72718018, 0., 0., 0.],
            [1.19992591, 0.65531457, 0., 2.11241287, 1.46718715, 0.]
        ])

        idf_expected = [0., 0., 0.40546511, 1.09861229, 1.09861229, 1.09861229]

        x_w_expected = [
            [0., 0., 0.34624155, 0., 0., 0.9381454],
            [0., 0., 0.34624155, 0., 0., 0.9381454],
            [0., 0., 0.34624155, 0., 0., 0.9381454],
            [0., 0., 1., 0., 0., 0.],
            [0., 0., 1., 0., 0., 0.],
            [0., 0., 1., 0., 0., 0.],
            [0., 0., 0., 0.83205029, 0.5547002, 0.],
            [0., 0., 0., 0.70710678, 0.70710678, 0.],
            [0., 0., 0., 0.89442719, 0.4472136, 0.]
        ]
        y_w_expected = ['A', 'A', 'A', 'B', 'B', 'B', 'C', 'C', 'C']
        x_name_w_expected = ['넷', '두', '셋', '여섯', '다섯', '하나']

        # Cluster value will change everytime! So don't rely on this
        x_clustered_expected = [
            [0., 0., 0.34624155, 0., 0., 0.9381454],
            [0., 0., 1., 0., 0., 0.],
            [0., 0., 0., 0.86323874, 0.5009569, 0.],
            [0., 0., 0., 0.70710678, 0.70710678, 0.]
        ]
        y_clustered_expected = [1, 2, 3, 3]

    def unit_test_predict_classes(
            self,
            include_match_details = False,
            top = 5
    ):
        log.Log.info(
            'Test predict classes using model "' + str(self.model_name) + '".'
        )

        model_obj = ModelHelper.get_model(
            model_name        = self.model_name,
            model_params      = None,
            identifier_string = self.identifier_string,
            dir_path_model    = self.ut_params.dirpath_model,
            training_data     = None
        )
        model_obj.start()
        model_obj.wait_for_model()
        #model_obj.load_model_parameters()

        test_x = UnitTestMetricSpaceModel.DATA_TEST_X
        test_x_name = UnitTestMetricSpaceModel.DATA_TEST_X_NAME
        model_x_name = model_obj.get_model_features()
        if model_x_name is None:
            model_x_name = UnitTestMetricSpaceModel.DATA_X_NAME

        if model_x_name.ndim == 2:
            model_x_name = model_x_name[0]
        log.Log.info(
            str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
            + ': Model x_name: ' + str(model_x_name)
        )

        # Reorder by model x_name
        df_x_name = pd.DataFrame(data={'word': model_x_name, 'target_order': range(0, len(model_x_name), 1)})
        df_test_x_name = pd.DataFrame(data={'word': test_x_name, 'original_order': range(0, len(test_x_name), 1)})
        # log.Log.debug('**** Target Order: ' + str(model_x_name))
        # log.Log.debug('**** Original order: ' + str(test_x_name))
        # Left join to ensure the order follows target order and target symbols
        df_x_name = df_x_name.merge(df_test_x_name, how='left')
        # log.Log.debug('**** Merged Order: ' + str(df_x_name))
        # Then order by original order
        df_x_name = df_x_name.sort_values(by=['target_order'], ascending=True)
        # Then the order we need to reorder is the target_order column
        reorder = np.array(df_x_name['original_order'])
        log.Log.debugdebug(
            str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
            + ': After reorder, df_x_name: ' + str(df_x_name)
        )
        log.Log.debugdebug(
            str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
            + ': After reorder, reorder: ' + str(reorder)
        )
        log.Log.debugdebug(
            str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
            + ': After reorder, test_x:' + str(test_x)
        )

        test_x_transpose = test_x.transpose()
        log.Log.debugdebug(test_x_transpose)

        reordered_test_x = np.zeros(shape=test_x_transpose.shape)
        log.Log.debugdebug(reordered_test_x)

        for i in range(0, reordered_test_x.shape[0], 1):
            reordered_test_x[i] = test_x_transpose[reorder[i]]

        reordered_test_x = reordered_test_x.transpose()
        log.Log.debugdebug(
            str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
            + ': Reordered test x = ' + str(reordered_test_x)
        )

        x_classes_expected = self.y
        # Just the top predicted ones
        all_y_observed_top = []
        all_y_observed = []
        mse = 0
        count_all = reordered_test_x.shape[0]

        log.Log.info(
            str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
            + ': Predict classes for x:\n\r' + str(reordered_test_x)
        )
        prf_start = prf.Profiling.start()

        for i in range(reordered_test_x.shape[0]):
            v = npUtil.NumpyUtil.convert_dimension(arr=reordered_test_x[i], to_dim=2)
            log.Log.info(
                str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
                + ': Testing x: ' + str(v)
            )
            if self.model_name == ModelHelper.MODEL_NAME_HYPERSPHERE_METRICSPACE:
                predict_result = model_obj.predict_class(
                    x           = v,
                    include_match_details = include_match_details,
                    top = top
                )
            else:
                predict_result = model_obj.predict_class(
                    x           = v
                )
            y_observed = predict_result.predicted_classes
            all_y_observed_top.append(y_observed[0])
            all_y_observed.append(y_observed)
            top_class_distance = predict_result.top_class_distance
            match_details = predict_result.match_details

            log.Log.info(
                str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
                + ': Point v ' + str(v) + ', predicted ' + str(y_observed)
                + ', Top Class Distance: ' + str(top_class_distance)
                + ', Match Details:\n\r' + str(match_details)
            )

            if self.model_name == ModelHelper.MODEL_NAME_HYPERSPHERE_METRICSPACE:
                metric = top_class_distance
                mse += metric ** 2

        prf_dur = prf.Profiling.get_time_dif(prf_start, prf.Profiling.stop())
        log.Log.important(
            str(self.__class__) + str(getframeinfo(currentframe()).lineno)
            + ' PROFILING ' + str(count_all) + ' calculations: ' + str(round(1000*prf_dur,0))
            + ', or ' + str(round(1000*prf_dur/count_all,2)) + ' milliseconds per calculation'
        )

        # Compare with expected
        compare_top_x = {}
        res_top1 = ResultObj(count_ok=0, count_fail=0)

        for t in range(1, top + 1, 1):
            # True or '1' means not correct or error
            compare_top_x[t] = np.array([True] * len(all_y_observed))
            for i in range(len(all_y_observed)):
                matches_i = all_y_observed[i]
                if x_classes_expected[i] in matches_i[0:t]:
                    # False of '0' means no error
                    compare_top_x[t][i] = False
                    res_top1.count_ok += 1*(t==1)
                else:
                    res_top1.count_fail += 1*(t==1)
            log.Log.info(compare_top_x[t])
            log.Log.info(
                'Total Errors (compare top #' + str(t) + ') = ' + str(np.sum(compare_top_x[t] * 1))
            )

        log.Log.info('mse = ' + str(mse))

        if self.model_name == ModelHelper.MODEL_NAME_HYPERSPHERE_METRICSPACE:
            predict_result = model_obj.predict_classes(
                    x           = reordered_test_x,
                    include_match_details = include_match_details,
                    top = top
                )
            log.Log.info('Predicted Classes:\n\r' + str(predict_result.predicted_classes))
            log.Log.info('Top class distance:\n\r' + str(predict_result.top_class_distance))
            log.Log.info('Match Details:\n\r' + str(predict_result.match_details))
            log.Log.info('MSE = ' + str(predict_result.mse))

        model_obj.join()
        return res_top1

    def run_unit_test(self):
        self.unit_test_train()

        res = self.unit_test_predict_classes(
            include_match_details = True,
            top = 2
        )
        return res


if __name__ == '__main__':
    config = Config.get_cmdline_params_and_init_config_singleton(
        Derived_Class = Config,
        default_config_file = Config.CONFIG_FILE_DEFAULT
    )
    ut_params = UnitTestParams(
        dirpath_wordlist     = config.get_config(param=Config.PARAM_NLP_DIR_WORDLIST),
        postfix_wordlist     = config.get_config(param=Config.PARAM_NLP_POSTFIX_WORDLIST),
        dirpath_app_wordlist = config.get_config(param=Config.PARAM_NLP_DIR_APP_WORDLIST),
        postfix_app_wordlist = config.get_config(param=Config.PARAM_NLP_POSTFIX_APP_WORDLIST),
        dirpath_synonymlist  = config.get_config(param=Config.PARAM_NLP_DIR_SYNONYMLIST),
        postfix_synonymlist  = config.get_config(param=Config.PARAM_NLP_POSTFIX_SYNONYMLIST),
        dirpath_model        = config.get_config(param=Config.PARAM_MODEL_DIR)
    )
    print('Unit Test Params: ' + str(ut_params.to_string()))

    log.Log.LOGLEVEL = log.Log.LOG_LEVEL_INFO

    for model_name in [
            ModelHelper.MODEL_NAME_HYPERSPHERE_METRICSPACE,
            #modelHelper.ModelHelper.MODEL_NAME_KERAS,
    ]:
        obj = UnitTestMetricSpaceModel(
            ut_params         = ut_params,
            model_name        = model_name
        )
        res = obj.run_unit_test()
        print('***** PASS ' + str(res.count_ok) + ', FAIL ' + str(res.count_fail))

