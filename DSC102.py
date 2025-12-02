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









TASK 3 HERE:

# %load -s task_3 assignment2.py
def task_3(data_io, product_data):
    # -----------------------------Column names--------------------------------
    # Inputs:
    asin_column = 'asin'
    price_column = 'price'
    attribute = 'also_viewed'
    related_column = 'related'
    # Outputs:
    meanPriceAlsoViewed_column = 'meanPriceAlsoViewed'
    countAlsoViewed_column = 'countAlsoViewed'
    # -------------------------------------------------------------------------

    # ---------------------- Your implementation begins------------------------

    also_viewed_df = product_data.select(
        F.col(asin_column).alias(asin_column),
        F.col(related_column).getItem(attribute).alias('also_viewed_array')
    )

    # 2) Compute countAlsoViewed
    #    - length of the also_viewed array
    #    - null if the array is null or empty
    also_viewed_df = also_viewed_df.withColumn(
        countAlsoViewed_column,
        F.when(
            F.col('also_viewed_array').isNull() |
            (F.size('also_viewed_array') == 0),
            F.lit(None).cast('int')
        ).otherwise(F.size('also_viewed_array'))
    )

    count_df = also_viewed_df.select(
        asin_column,
        countAlsoViewed_column
    )

    # 3) Compute meanPriceAlsoViewed
    #    - explode also_viewed_array to individual ASINs
    #    - join to product_data on asin to get prices
    #    - ignore dangling references and rows where price is null
    #    - keep products with price == 0
    exploded_df = also_viewed_df.select(
        F.col(asin_column),
        F.explode_outer('also_viewed_array').alias('also_asin')
    )

    product_prices = product_data.select(
        F.col(asin_column).alias('asin_price'),
        F.col(price_column).alias(price_column)
    )

    joined_prices = (
        exploded_df
        .join(product_prices,
              exploded_df['also_asin'] == product_prices['asin_price'],
              how='inner')
        .filter(F.col(price_column).isNotNull())
    )

    mean_price_df = (
        joined_prices
        .groupBy(asin_column)
        .agg(F.avg(price_column).alias(meanPriceAlsoViewed_column))
    )

    # 4) Attach the new columns back to the original product_data
    product_with_related = (
        product_data
        .join(mean_price_df, on=asin_column, how='left')
        .join(count_df, on=asin_column, how='left')
    )



    # -------------------------------------------------------------------------

    # ---------------------- Put results in res dict --------------------------
    res = {
        'count_total': None,
        'mean_meanPriceAlsoViewed': None,
        'variance_meanPriceAlsoViewed': None,
        'numNulls_meanPriceAlsoViewed': None,
        'mean_countAlsoViewed': None,
        'variance_countAlsoViewed': None,
        'numNulls_countAlsoViewed': None
    }
    # Modify res:

    count_total = product_with_related.count()

    # Aggregate statistics (nulls are ignored automatically)
    stats_row = product_with_related.agg(
        F.mean(meanPriceAlsoViewed_column).alias('mean_meanPriceAlsoViewed'),
        F.variance(meanPriceAlsoViewed_column).alias('variance_meanPriceAlsoViewed'),
        F.mean(countAlsoViewed_column).alias('mean_countAlsoViewed'),
        F.variance(countAlsoViewed_column).alias('variance_countAlsoViewed')
    ).collect()[0]

    # Null counts
    num_nulls_mean = product_with_related.filter(
        F.col(meanPriceAlsoViewed_column).isNull()
    ).count()

    num_nulls_count = product_with_related.filter(
        F.col(countAlsoViewed_column).isNull()
    ).count()

    # Fill res with native Python types
    res['count_total'] = int(count_total)

    mean_mean = stats_row['mean_meanPriceAlsoViewed']
    var_mean = stats_row['variance_meanPriceAlsoViewed']
    mean_count = stats_row['mean_countAlsoViewed']
    var_count = stats_row['variance_countAlsoViewed']

    res['mean_meanPriceAlsoViewed'] = float(mean_mean) if mean_mean is not None else None
    res['variance_meanPriceAlsoViewed'] = float(var_mean) if var_mean is not None else None
    res['mean_countAlsoViewed'] = float(mean_count) if mean_count is not None else None
    res['variance_countAlsoViewed'] = float(var_count) if var_count is not None else None

    res['numNulls_meanPriceAlsoViewed'] = int(num_nulls_mean)
    res['numNulls_countAlsoViewed'] = int(num_nulls_count)


    # -------------------------------------------------------------------------

    # ----------------------------- Do not change -----------------------------
    data_io.save(res, 'task_3')
    return res
    # -------------------------------------------------------------------------


# %load -s task_4 assignment2.py
def task_4(data_io, product_data):
    # -----------------------------Column names--------------------------------
    # Inputs:
    price_column = 'price'
    title_column = 'title'
    # Outputs:
    meanImputedPrice_column = 'meanImputedPrice'
    medianImputedPrice_column = 'medianImputedPrice'
    unknownImputedTitle_column = 'unknownImputedTitle'
    # -------------------------------------------------------------------------
    
    from pyspark.sql import functions as F
    from pyspark.sql.types import FloatType
    
    # ---------------------- Your implementation begins------------------------
    
    # 1. Cast price to float and calculate mean for imputation
    df_with_float = product_data.withColumn("price_float", F.col(price_column).cast(FloatType()))
    
    # Calculate mean of non-null price values
    mean_price = df_with_float.select(F.mean("price_float")).first()[0]
    
    # Impute nulls with mean
    df_mean_imputed = df_with_float.withColumn(
        meanImputedPrice_column,
        F.when(F.col("price_float").isNull(), mean_price).otherwise(F.col("price_float"))
    )
    
    # 2. Calculate median and impute
    median_price = df_with_float.select(
        F.expr("percentile_approx(price_float, 0.5)")
    ).first()[0]
    
    df_median_imputed = df_mean_imputed.withColumn(
        medianImputedPrice_column,
        F.when(F.col("price_float").isNull(), median_price).otherwise(F.col("price_float"))
    )
    
    # 3. Impute title with 'unknown' for nulls and empty strings
    df_final = df_median_imputed.withColumn(
        unknownImputedTitle_column,
        F.when(
            (F.col(title_column).isNull()) | (F.trim(F.col(title_column)) == ""),
            "unknown"
        ).otherwise(F.col(title_column))
    )
    
    # 4. Calculate statistics
    stats = df_final.select(
        F.count("*").alias("count_total"),
        F.mean(meanImputedPrice_column).alias("mean_meanImputedPrice"),
        F.variance(meanImputedPrice_column).alias("variance_meanImputedPrice"),
        F.sum(F.when(F.col(meanImputedPrice_column).isNull(), 1).otherwise(0)).alias("numNulls_meanImputedPrice"),
        F.mean(medianImputedPrice_column).alias("mean_medianImputedPrice"),
        F.variance(medianImputedPrice_column).alias("variance_medianImputedPrice"),
        F.sum(F.when(F.col(medianImputedPrice_column).isNull(), 1).otherwise(0)).alias("numNulls_medianImputedPrice"),
        F.sum(F.when(F.col(unknownImputedTitle_column) == "unknown", 1).otherwise(0)).alias("numUnknowns_unknownImputedTitle")
    ).first()
    
    # ---------------------- Put results in res dict --------------------------
    res = {
        'count_total': stats["count_total"],
        'mean_meanImputedPrice': stats["mean_meanImputedPrice"],
        'variance_meanImputedPrice': stats["variance_meanImputedPrice"],
        'numNulls_meanImputedPrice': stats["numNulls_meanImputedPrice"],
        'mean_medianImputedPrice': stats["mean_medianImputedPrice"],
        'variance_medianImputedPrice': stats["variance_medianImputedPrice"],
        'numNulls_medianImputedPrice': stats["numNulls_medianImputedPrice"],
        'numUnknowns_unknownImputedTitle': float(stats["numUnknowns_unknownImputedTitle"])
    }
    # -------------------------------------------------------------------------
    
    # ----------------------------- Do not change -----------------------------
    data_io.save(res, 'task_4')
    return res
    # -------------------------------------------------------------------------













# %load -s task_5 assignment2.py
def task_5(data_io, product_processed_data, word_0, word_1, word_2):
    # -----------------------------Column names--------------------------------
    # Inputs:
    title_column = 'title'
    # Outputs:
    titleArray_column = 'titleArray'
    titleVector_column = 'titleVector'
    # -------------------------------------------------------------------------

    # ---------------------- Your implementation begins------------------------

    product_processed_data_output = product_processed_data.withColumn(
        titleArray_column,
        F.split(F.lower(F.col(title_column)), ' ')
    )

    # 2) Train Word2Vec on titleArray
    word2vec = M.feature.Word2Vec(
        inputCol=titleArray_column,
        outputCol=titleVector_column,
        vectorSize=16,
        minCount=100,
        numPartitions=4,
        seed=SEED
    )
    model = word2vec.fit(product_processed_data_output)

    # 3) Transform to add titleVector column (even if not directly used later)
    product_processed_data_output = model.transform(product_processed_data_output)



    # -------------------------------------------------------------------------

    # ---------------------- Put results in res dict --------------------------
    res = {
        'count_total': None,
        'size_vocabulary': None,
        'word_0_synonyms': [(None, None), ],
        'word_1_synonyms': [(None, None), ],
        'word_2_synonyms': [(None, None), ]
    }
    # Modify res:
    res['count_total'] = product_processed_data_output.count()
    res['size_vocabulary'] = model.getVectors().count()
    for name, word in zip(
        ['word_0_synonyms', 'word_1_synonyms', 'word_2_synonyms'],
        [word_0, word_1, word_2]
    ):
        res[name] = model.findSynonymsArray(word, 10)
    # -------------------------------------------------------------------------

    # ----------------------------- Do not change -----------------------------
    data_io.save(res, 'task_5')
    return res
    # -------------------------------------------------------------------------





























# %load -s task_6 assignment2.py
def task_6(data_io, product_processed_data):
    # -----------------------------Column names--------------------------------
    # Inputs:
    category_column = 'category'
    # Outputs:
    categoryIndex_column = 'categoryIndex'
    categoryOneHot_column = 'categoryOneHot'
    categoryPCA_column = 'categoryPCA'
    # -------------------------------------------------------------------------    
    
    from pyspark.sql import functions as F
    from pyspark.ml.feature import StringIndexer, OneHotEncoder, PCA
    from pyspark.ml.stat import Summarizer
    
    # ---------------------- Your implementation begins------------------------
    
    # Step 1: One-hot encode the category column
    # First, use StringIndexer to convert string categories to numerical indices
    # Use handleInvalid='skip' to avoid creating an extra index for unseen values
    # or use default behavior which only indexes seen values during fit
    indexer = StringIndexer(
        inputCol=category_column,
        outputCol=categoryIndex_column
    )
    
    # Fit the indexer and transform the data
    indexer_model = indexer.fit(product_processed_data)
    df_indexed = indexer_model.transform(product_processed_data)
    
    # One-hot encode the indexed column
    # Set dropLast=False to ensure dimension equals the size of domain
    encoder = OneHotEncoder(
        inputCol=categoryIndex_column,
        outputCol=categoryOneHot_column,
        dropLast=False
    )
    
    encoder_model = encoder.fit(df_indexed)
    df_encoded = encoder_model.transform(df_indexed)
    
    # Step 2: Apply PCA to reduce dimension to 15
    pca = PCA(
        k=15,  # Reduce to 15 dimensions
        inputCol=categoryOneHot_column,
        outputCol=categoryPCA_column
    )
    
    pca_model = pca.fit(df_encoded)
    df_pca = pca_model.transform(df_encoded)
    
    # Step 3: Calculate statistics
    # Count total rows
    count_total = df_pca.count()
    
    # Calculate mean vectors using Summarizer
    # For categoryOneHot
    summary_onehot = df_pca.select(
        Summarizer.mean(F.col(categoryOneHot_column)).alias("mean_onehot")
    ).first()
    
    mean_vector_onehot = summary_onehot["mean_onehot"]
    # Convert to dense representation and then to list
    meanVector_categoryOneHot = mean_vector_onehot.toArray().tolist()
    
    # For categoryPCA
    summary_pca = df_pca.select(
        Summarizer.mean(F.col(categoryPCA_column)).alias("mean_pca")
    ).first()
    
    mean_vector_pca = summary_pca["mean_pca"]
    # Convert to dense representation and then to list
    meanVector_categoryPCA = mean_vector_pca.toArray().tolist()
    
    # -------------------------------------------------------------------------
    res = {
        'count_total': count_total,
        'meanVector_categoryOneHot': meanVector_categoryOneHot,
        'meanVector_categoryPCA': meanVector_categoryPCA
    }
    # -------------------------------------------------------------------------
    
    # ----------------------------- Do not change -----------------------------
    data_io.save(res, 'task_6')
    return res
    # -------------------------------------------------------------------------











def task_7(data_io, train_data, test_data):
    # ---------------------- Your implementation begins------------------------
    features_col = 'features'
    label_col = 'overall'
    prediction_col = 'prediction'

    # 1. Define and train Decision Tree Regressor with maxDepth = 5
    dt = M.regression.DecisionTreeRegressor(
        featuresCol=features_col,
        labelCol=label_col,
        predictionCol=prediction_col,
        maxDepth=5
    )
    model = dt.fit(train_data)

    # 2. Predict on test data
    predictions = model.transform(test_data)

    # 3. Evaluate RMSE on test predictions
    evaluator = M.evaluation.RegressionEvaluator(
        labelCol=label_col,
        predictionCol=prediction_col,
        metricName='rmse'
    )
    test_rmse = evaluator.evaluate(predictions)
    # -------------------------------------------------------------------------

    # ---------------------- Put results in res dict --------------------------
    res = {
        'test_rmse': float(test_rmse)
    }
    # -------------------------------------------------------------------------

    # ----------------------------- Do not change -----------------------------
    data_io.save(res, 'task_7')
    return res
    # -------------------------------------------------------------------------

