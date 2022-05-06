# from logging_details.custom_logging import ApplicationLogging
#
# log = ApplicationLogging()
#
# class Sumegh:
#     def __init__(self):
#         log.Info("Sumegh is started")
#         pass
#
#     def Hi(self):
#         try:
#             a = 4/0
#             print(a)
#         except Exception as e:
#             log.Error("(Hi) :: "+ str(e))
#
# s = Sumegh()
# s.Hi()

from input_data_validation.validation import DataValidation
dv = DataValidation()

dv.checkingCategoricalColumns()