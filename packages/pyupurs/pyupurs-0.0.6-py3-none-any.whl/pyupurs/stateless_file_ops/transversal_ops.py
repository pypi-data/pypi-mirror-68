import csv


def count_cols_per_row(file_path: str, delimiter=",") -> dict:
    """
    In a structured delimiter-separated file, count the number of columns per row.
    Note : This function operates without loading the file in memory.

    :param file_path: Path of the file to process.
    :param delimiter: Delimiter used within the file
    :return: A dictionary for which the keys are the index of the row, and the value are its number of columns.
    """
    # TODO : Unit test this.
    # TODO : This shit is not stateless, it gives MemoryErrors... Use a csv.writer instead.
    with open(file_path, "r") as file:
        f_obj = csv.reader(file, delimiter=delimiter)
        col_count = [len(f) for f in f_obj]
        dict_col_count = {i: list_v for i, list_v in enumerate(col_count)}

        return dict_col_count


def count_rows(file_path: str, delimiter="|", count_header=True) -> int:
    """
    Count the number of rows in a structured separated file.
    Note : This function operates without loading the file in memory.

    :param file_path:
    :param delimiter:
    :param count_header:
    :return: The number of rows.
    """
    # TODO : Unit test this
    with open(file_path, "r") as file:
        f_obj = csv.reader(file, delimiter=delimiter)
        row_count = sum(1 for row in f_obj)
        if not count_header:
            row_count -= 1

        return row_count
