import os
from copy import copy

import xlsxwriter

from .commons import run_requests
from .consts import RED_TO_GREEN_GRADIENT
from ..services.services import Services


def convert_to_xlsx(
    input_path: str, services: Services, workers: int = 1, output_path: str = None,
):
    """Sends requests to defined Hypatos services for every invoice found in given
    directory. Merges results off all services into one Excel file and writes to
    project directory. Every key, value pair from Invoice Extractor will flattened
    into the following tuple:

        key = (value, probability, validation[optional])

    Arguments:
        path {str} -- Path to the directory containing invoices, uses rglob.
        extractor_endpoint {str} -- Url of Hypatos extractor service.

    Keyword Arguments:
        vat_validator_endpoint {str} -- Url of vat_validator. (default: {None})
        validation_endpoint {str} -- Url of validation. (default: {None})
        token {str} -- API token. (default: {None})
        workers {int} -- Amount of multithread. (default: {3})
    """
    if not output_path:
        output_path = f"{os.path.normpath(input_path).split(os.path.sep)[-1]}.xlsx"
    else:
        output_path = f"{os.path.join(os.getcwd(), output_path)}"
        if not os.path.isdir(os.path.sep.join(output_path.split(os.path.sep)[:-1])):
            quit("Output directory does not exsist")

    # Get requests result
    (
        result,
        single_fieldnames,
        multi_fieldnames,
        default_cols,
        vat_validation_result,
    ) = run_requests(workers, input_path, services)

    # Structure result
    single_cardinality, multi_cardinality = structure_cardinality(
        result, single_fieldnames, multi_fieldnames
    )

    # Init workbook/sheets
    workbook = xlsxwriter.Workbook(output_path)
    workbook.add_worksheet("single_cardinality")
    workbook.add_worksheet("multi_cardinality")

    # Styling
    header = workbook.add_format({"bold": True})
    probability_format = [
        workbook.add_format({"bold": True, "bg_color": color})
        for color in RED_TO_GREEN_GRADIENT
    ]

    write_single_cardinality(
        workbook,
        single_cardinality,
        header,
        probability_format,
        default_cols,
        services.validation_endpoint,
    )

    write_multi_cardinality(
        workbook,
        multi_cardinality,
        header,
        probability_format,
        default_cols,
        services.validation_endpoint,
    )

    if vat_validation_result:
        write_vat_validation(vat_validation_result, workbook)

    workbook.close()


def collect_column_names(extracted_invoice, single_fieldnames, multi_fieldnames):
    """Iterate through extracted invoice and write fieldnames to single or multi
    cardinality

    Arguments:
        extracted_invoice {[type]} -- [description]
        multi_fieldnames {[type]} -- [description]
        single_fieldnames {[type]} -- [description]
    """
    for col_name in extracted_invoice.keys():
        if col_name[-1].isdigit():
            label = "_".join(col_name.split("_")[:-1])
            multi_fieldnames[label] = (None, None, None)
        else:
            single_fieldnames[col_name] = (None, None, None)


def structure_cardinality(result, single_fieldnames, multi_fieldnames):
    """Structure the extracted invoice in different cardinalities.

    Arguments:
        result {[type]} -- [description]
        single_fieldnames {[type]} -- [description]
        multi_fieldnames {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    single_cardinality = {}
    multi_cardinality = {}

    for idx, invoice in result.items():
        single_item = copy(single_fieldnames)
        multi_items = {}

        for col, value in invoice.items():
            if col[-1].isdigit():
                num = int(col.split("_")[-1]) + 1
                label = "_".join(col.split("_")[:-1])
                if num not in multi_items:
                    multi_item = copy(multi_fieldnames)
                    multi_item["file_name"] = invoice["file_name"]
                    multi_item["row_number"] = (num, None, None)
                    multi_items[num] = multi_item

                multi_items[num][label] = invoice[col]
            else:
                single_item[col] = invoice[col]

        single_cardinality[idx] = single_item
        multi_cardinality[idx] = multi_items

    return single_cardinality, multi_cardinality


def write_single_cardinality(
    workbook,
    single_cardinality,
    bold_header,
    red_to_green_formats,
    default_cols,
    validation_endpoint,
):
    """Write single cardinality items to workbook.

    Arguments:
        workbook {[type]} -- [description]
        single_cardinality {[type]} -- [description]
        bold_header {[type]} -- [description]
        red_to_green_formats {[type]} -- [description]
        non_validation_cols {[type]} -- [description]
    """
    worksheet = workbook.get_worksheet_by_name("single_cardinality")

    for idx, row in single_cardinality.items():
        count = 0
        for key, value in row.items():
            worksheet.write(0, count, key, bold_header)
            column_value, probability, validation_errors = value

            if probability:
                color_idx = int((len(red_to_green_formats) - 1) * probability)
                color = red_to_green_formats[color_idx]
                worksheet.write(idx + 1, count, column_value, color)
            else:
                worksheet.write(idx + 1, count, column_value)

            if validation_endpoint and key not in default_cols:
                validation_errors = validation_errors if validation_errors else 0
                count += 1
                worksheet.write(0, count, f"{key}ValidationErrors", bold_header)
                if validation_errors == 0:
                    worksheet.write(idx + 1, count, validation_errors)
                else:
                    worksheet.write(idx + 1, count, len(validation_errors))
                    worksheet.write_comment(idx + 1, count, str(validation_errors))

            count += 1


def write_multi_cardinality(
    workbook,
    multi_cardinality,
    bold_header,
    red_to_green_formats,
    default_cols,
    validation_endpoint,
):
    """Write multi cardinality items to workbook.

    Arguments:
        workbook {[type]} -- [description]
        multi_cardinality {[type]} -- [description]
        bold_header {[type]} -- [description]
        red_to_green_formats {[type]} -- [description]
        non_validation_cols {[type]} -- [description]
    """
    worksheet = workbook.get_worksheet_by_name("multi_cardinality")
    item_count = 1

    for idx, row in multi_cardinality.items():
        for row_number, row_item in row.items():
            count = 0
            for key, value in row_item.items():
                worksheet.write(0, count, key, bold_header)
                column_value, probability, validation_errors = value

                if probability:
                    color_idx = int((len(red_to_green_formats) - 1) * probability)
                    color = red_to_green_formats[color_idx]
                    worksheet.write(item_count, count, column_value, color)
                else:
                    worksheet.write(item_count, count, column_value)

                if validation_endpoint and key not in default_cols:
                    validation_errors = validation_errors if validation_errors else 0
                    count += 1
                    worksheet.write(0, count, f"{key}ValidationErrors", bold_header)
                    if validation_errors == 0:
                        worksheet.write(item_count, count, validation_errors)
                    else:
                        worksheet.write(item_count, count, len(validation_errors))
                        worksheet.write_comment(
                            item_count, count, str(validation_errors)
                        )

                count += 1
            item_count += 1


def flatten_invoice(invoice, validation):
    return_dict = dict()
    entities = invoice["entities"]
    probabilities = invoice["probabilities"]

    def traverse_items(entities, probabilities, validation, _dict, *prefix):
        for k, v in entities.items():
            if isinstance(v, dict):
                traverse_items(
                    entities[k],
                    probabilities[k],
                    validation[k][0] if validation and k in validation else None,
                    return_dict,
                    k,
                )
            elif isinstance(v, list):
                for counter, list_item in enumerate(v):
                    # TODO: fix terms and ibanAll
                    if k != "terms" and k != "ibanAll":
                        temp_dict = {}
                        for item, value in list_item.items():
                            temp_dict[f"{k}_{item}_{counter}"] = value
                        traverse_items(
                            temp_dict,
                            probabilities[k][counter],
                            validation[k][0][str(counter)][0]
                            if validation
                            and k in validation
                            and str(counter) in validation[k][0]
                            else None,
                            return_dict,
                        )
            else:
                try:
                    # dirty solution, assumes no invoice extractor response field got underscore
                    original_k = k.split("_")[-2]
                except IndexError:
                    original_k = k

                if prefix:
                    field_name = f"{prefix[0]}_{k}"
                else:
                    field_name = k

                if original_k in probabilities:
                    if probabilities[original_k]:
                        _dict[field_name] = (v, probabilities[original_k], None)
                    else:
                        _dict[field_name] = (v, None, None)
                else:
                    _dict[field_name] = (v, None, None)
                if validation:
                    if original_k in validation:
                        _dict[field_name] = (v, None, validation[original_k])

    traverse_items(entities, probabilities, validation, return_dict)
    return return_dict


def write_vat_validation(result, workbook):
    workbook.add_worksheet("vat_validation")
    worksheet = workbook.get_worksheet_by_name("vat_validation")

    for idx, row in result.items():
        count = 0
        for key, value in row.items():
            worksheet.write(0, count, key)
            worksheet.write(idx + 1, count, value)
            count += 1
