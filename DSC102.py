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







TASK 2 HERE:

# %load -s task_2 assignment2.py
def task_2(data_io, product_data):
    # -----------------------------Column names--------------------------------
    # Inputs:
    salesRank_column = 'salesRank'
    categories_column = 'categories'
    asin_column = 'asin'
    # Outputs:
    category_column = 'category'
    bestSalesCategory_column = 'bestSalesCategory'
    bestSalesRank_column = 'bestSalesRank'
    # -------------------------------------------------------------------------

    # ---------------------- Your implementation begins------------------------

    extracted_category = F.col(categories_column).getItem(0).getItem(0)
    
    product_flat = (
        product_data.withColumn(
            category_column,
            F.when(
                (extracted_category.isNull()) | (extracted_category == ""), 
                F.lit(None)
            ).otherwise(extracted_category)
        )
    )

    # 2) Flatten salesRank map into bestSalesCategory (key) and bestSalesRank (value)
    sr_col = F.col(salesRank_column)
    product_flat = (
        product_flat
        .withColumn(
            bestSalesCategory_column,
            F.when(
                sr_col.isNull() | (F.size(F.map_keys(sr_col)) == 0),
                F.lit(None)
            ).otherwise(
                F.map_keys(sr_col).getItem(0)
            )
        )
        .withColumn(
            bestSalesRank_column,
            F.when(
                sr_col.isNull() | (F.size(F.map_values(sr_col)) == 0),
                F.lit(None)
            ).otherwise(
                F.map_values(sr_col).getItem(0)
            )
        )
    )



    # -------------------------------------------------------------------------

    # ---------------------- Put results in res dict --------------------------
    res = {
        'count_total': None,
        'mean_bestSalesRank': None,
        'variance_bestSalesRank': None,
        'numNulls_category': None,
        'countDistinct_category': None,
        'numNulls_bestSalesCategory': None,
        'countDistinct_bestSalesCategory': None
    }
    # Modify res:

    count_total = product_flat.count()

    # Mean and variance of bestSalesRank (nulls ignored automatically by agg functions)
    stats_row = product_flat.agg(
        F.mean(bestSalesRank_column).alias('mean_bestSalesRank'),
        F.variance(bestSalesRank_column).alias('variance_bestSalesRank')
    ).collect()[0]

    # Null counts
    num_nulls_category = product_flat.filter(F.col(category_column).isNull()).count()
    num_nulls_bestSalesCategory = product_flat.filter(F.col(bestSalesCategory_column).isNull()).count()

    # Distinct counts excluding nulls
    count_distinct_category = (
        product_flat
        .select(category_column)
        .where(F.col(category_column).isNotNull())
        .distinct()
        .count()
    )

    count_distinct_bestSalesCategory = (
        product_flat
        .select(bestSalesCategory_column)
        .where(F.col(bestSalesCategory_column).isNotNull())
        .distinct()
        .count()
    )

    # Fill res with native Python types
    res['count_total'] = int(count_total)

    mean_bsr = stats_row['mean_bestSalesRank']
    var_bsr = stats_row['variance_bestSalesRank']

    res['mean_bestSalesRank'] = float(mean_bsr) if mean_bsr is not None else None
    res['variance_bestSalesRank'] = float(var_bsr) if var_bsr is not None else None

    res['numNulls_category'] = int(num_nulls_category)
    res['countDistinct_category'] = int(count_distinct_category)
    res['numNulls_bestSalesCategory'] = int(num_nulls_bestSalesCategory)
    res['countDistinct_bestSalesCategory'] = int(count_distinct_bestSalesCategory)


    # -------------------------------------------------------------------------

    # ----------------------------- Do not change -----------------------------
    data_io.save(res, 'task_2')
    return res
    # -------------------------------------------------------------------------

