import os
import csv
import pandas as pd

from pyupurs.exceptions.FileIsEmptyError import FileIsEmptyError
from pyupurs.stateless_file_ops.transversal_ops import count_cols_per_row


def audit_extra_separators(file_path: str, delimiter: str = ",", number_of_columns: int = None):
    """
    Construct a report of faulty rows in regards to badly delimited data.

    :param file_path: path towards the file. It has to be a structured delimited data file, such as csv.
    :param delimiter: separator of columns within the data file
    :param number_of_columns: number of known columns in the schema.
        If not specified, the number of columns will be calculated by counting the number of columns per row,
        then taking the number of columns that appears the most.
    :return: A dataframe with the faulty row information.
    """

    # Check file existence
    if not os.path.isfile(file_path):
        raise FileNotFoundError

    # Check if file is empty
    if not os.path.getsize(file_path) > 0:
        raise FileIsEmptyError(f"The file {file_path} is completely empty.")

    # rows_n_cols = count_cols_per_row(file_path, delimiter=delimiter)

    # if not number_of_columns:
    ## Estimate of the number of cols. Assuming the most frequent col count is a valid criterion.
    # number_of_columns = pd.Series(rows_n_cols).value_counts().idxmax()

    # list_rows_n_cols = rows_n_cols.values()

    # n_col_occurrences = len(set(list_rows_n_cols))

    abnormal_rows = []
    with open(file_path, "r") as file, open("faulty_rows.csv", "w") as writer:
        f_object = csv.reader(file, delimiter=delimiter)
        f_write_object = csv.writer(writer, delimiter="|")
        # Engage in defective row extraction only if the column count is suspicious
        # if n_col_occurrences > 1:
        # [abnormal_rows.append(row) for row in f_object if len(row) != number_of_columns]
        [f_write_object.writerow(row) for row in f_object if len(row) != number_of_columns]

    # defective_df = pd.DataFrame(data=abnormal_rows)  # columns=header
    # return defective_df
#
#
# if __name__ == "__main__":
#     audit_extra_separators("../../tests/samples/stateless_file_ops/auditing_ops/audit_extra_separators_e2.csv",
#                            delimiter="|", number_of_columns=4)
#
