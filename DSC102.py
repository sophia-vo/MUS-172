# %load -s task_1 assignment2.py
def task_1(data_io, review_data, product_data):
    # -----------------------------Column names--------------------------------
    # Inputs:
    asin_column = 'asin'
    overall_column = 'overall'
    # Outputs:
    mean_rating_column = 'meanRating'
    count_rating_column = 'countRating'
    # -------------------------------------------------------------------------

    # ---------------------- Your implementation begins------------------------

    review_agg = (review_data
        .groupBy(asin_column)
        .agg(
            F.avg(overall_column).alias(mean_rating_column),
            F.count(overall_column).alias(count_rating_column)
        )
    )


    joined_df = (
        product_data
        .select(asin_column)
        .join(review_agg, on=asin_column, how='left'))



    # -------------------------------------------------------------------------

    # ---------------------- Put results in res dict --------------------------
    # Calculate the values programmaticly. Do not change the keys and do not
    # hard-code values in the dict. Your submission will be evaluated with
    # different inputs.
    # Modify the values of the following dictionary accordingly.
    res = {
        'count_total': None,
        'mean_meanRating': None,
        'variance_meanRating': None,
        'numNulls_meanRating': None,
        'mean_countRating': None,
        'variance_countRating': None,
        'numNulls_countRating': None
    }
    # Modify res:
    count_total = joined_df.count()

    stats_row = joined_df.agg(
        F.mean(mean_rating_column).alias('mean_meanRating'),
        F.variance(mean_rating_column).alias('variance_meanRating'),
        F.mean(count_rating_column).alias('mean_countRating'),
        F.variance(count_rating_column).alias('variance_countRating')
    ).collect()[0]

    num_nulls_mean = joined_df.filter(F.col(mean_rating_column).isNull()).count()
    num_nulls_count = joined_df.filter(F.col(count_rating_column).isNull()).count()

    res['count_total'] = int(count_total)

    mean_mean = stats_row['mean_meanRating']
    var_mean = stats_row['variance_meanRating']
    mean_count = stats_row['mean_countRating']
    var_count = stats_row['variance_countRating']

    res['mean_meanRating'] = float(mean_mean) if mean_mean is not None else None
    res['variance_meanRating'] = float(var_mean) if var_mean is not None else None
    res['mean_countRating'] = float(mean_count) if mean_count is not None else None
    res['variance_countRating'] = float(var_count) if var_count is not None else None

    res['numNulls_meanRating'] = int(num_nulls_mean)
    res['numNulls_countRating'] = int(num_nulls_count)


    # -------------------------------------------------------------------------

    # ----------------------------- Do not change -----------------------------
    data_io.save(res, 'task_1')
    return res
    # -------------------------------------------------------------------------
