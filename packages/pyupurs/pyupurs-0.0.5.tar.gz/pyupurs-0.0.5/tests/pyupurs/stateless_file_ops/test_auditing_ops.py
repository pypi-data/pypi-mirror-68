import pytest
import pandas

from pyupurs.exceptions.FileIsEmptyError import FileIsEmptyError
from pyupurs.stateless_file_ops.auditing_ops import audit_extra_separators


def test_audit_extra_separators():
    """
        Test case -> Awaited result :

        Definitions :
        Let c_ncols the correct number of columns in a file.
        A - Empty rows
        B - Non-empty rows
        C - Rows with protected strings & delimiters within the strings

        - For parameter : "file_path" & the contents of its data :
            - No file -> FileNotFound Exception
            - Empty file -> Or empty pandas.Dataframe
            - Empty file except header -> Empty pandas.Dataframe
            - rows where n_cols == c_ncols for cases A, B & C. -> Empty pandas.Dataframe
            - rows where n_cols < c_ncols ->  ??
            - rows where ncols > c_ncols -> pandas.Dataframe with the faulty rows
        - For parameter : delimiter
            - None
            - Wrong delimiter
            - Right delimiter

        - For parameter : number_of_columns :
            - None
            - number_of_columns == c_ncols
            - number_of_columns > c_ncols
            - number_of_columns < c_ncols
            - number_of_columns == 0
    """
    # Files :
    file_nan = "tests/samples/stateless_file_ops/auditing_ops/audit_extra_separators_enan.csv"
    file_0 = "tests/samples/stateless_file_ops/auditing_ops/audit_extra_separators_e0.csv"
    file_1 = "tests/samples/stateless_file_ops/auditing_ops/audit_extra_separators_e1.csv"
    file_2 = "tests/samples/stateless_file_ops/auditing_ops/audit_extra_separators_e2.csv"
    df_empty = pandas.DataFrame()

    df_original = pandas.DataFrame(data={0: ["h1", "A", "dq", "ho", "one", "em1", "ab", "da"],
                                         1: ["h2", "B", "dr", "hi", "two", "em2", "bc", "di"],
                                         2: ["h3", "C", "de", "ha", "three", None, "cd", None],
                                         3: ["h4", "D", "da", "hu", "", None, "de", None],
                                         4: [None, "R", None, "Are you kidding me", None, None, None, None],
                                         5: [None, None, None, "my | nigga", None, None, None, None],
                                         })

    df_results2 = pandas.DataFrame(data={0: ["h1", "dq", "ho", "one", "em1", "ab", "da"],
                                         1: ["h2", "dr", "hi", "two", "em2", "bc", "di"],
                                         2: ["h3", "de", "ha", "three", None, "cd", None],
                                         3: ["h4", "da", "hu", "", None, "de", None],
                                         4: [None, None, "Are you kidding me", None, None, None, None],
                                         5: [None, None, "my | nigga", None, None, None, None],
                                         })

    df_results1 = pandas.DataFrame(data={0: ["A", "ho", "em1", "da"],
                                         1: ["B", "hi", "em2", "di"],
                                         2: ["C", "ha", None, None],
                                         3: ["D", "hu", None, None],
                                         4: ["R", "Are you kidding me", None, None],
                                         5: [None, "my | nigga", None, None]
                                         })

    # parameter : file_path
    with pytest.raises(FileNotFoundError):
        audit_extra_separators(file_path=file_nan, delimiter="|")

    with pytest.raises(FileIsEmptyError):
        audit_extra_separators(file_path=file_0, delimiter="|")

    assert (df_empty.equals(audit_extra_separators(file_path=file_1, delimiter="|")))
    assert (df_results1.equals(audit_extra_separators(file_path=file_2, delimiter="|")))

    # parameter : delimiter
    with pytest.raises(TypeError):
        audit_extra_separators(file_path=file_2, delimiter=None)

    wrong_delim_df = audit_extra_separators(file_path=file_2, delimiter=",")
    assert (df_empty.equals(wrong_delim_df))

    right_delim_df = audit_extra_separators(file_path=file_2, delimiter="|")
    assert (df_results1.equals(right_delim_df))

    # parameter : number_of_columns

    none_num_cols_df = audit_extra_separators(file_path=file_2, delimiter="|", number_of_columns=None)
    assert (df_results1.equals(none_num_cols_df))
    equal_num_cols_df = audit_extra_separators(file_path=file_2, delimiter="|", number_of_columns=4)
    assert (df_results1.equals(equal_num_cols_df))
    sup_num_cols_df = audit_extra_separators(file_path=file_2, delimiter="|", number_of_columns=5)
    assert (df_results2.equals(sup_num_cols_df))
    inf_num_cols_df = audit_extra_separators(file_path=file_2, delimiter="|", number_of_columns=3)
    assert (df_original.equals(inf_num_cols_df))
    zero_num_cols_df = audit_extra_separators(file_path=file_2, delimiter="|", number_of_columns=0)
    assert (df_results1.equals(zero_num_cols_df))
