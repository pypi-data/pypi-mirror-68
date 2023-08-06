# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Various constants used throughout AutoML."""


class FeaturizationConfigMode:
    Auto = 'auto'
    Off = 'off'
    Customized = 'customized'


class FeatureType:
    """Names for feature types that are recognized."""

    Numeric = 'Numeric'
    DateTime = 'DateTime'
    Categorical = 'Categorical'
    CategoricalHash = 'CategoricalHash'
    Text = 'Text'
    Hashes = 'Hashes'
    Ignore = 'Ignore'
    AllNan = 'AllNan'

    FULL_SET = {Numeric, DateTime, Categorical, CategoricalHash, Text, Hashes, Ignore, AllNan}

    # List of features types that are dropped and not featurized
    DROP_SET = {Hashes, Ignore, AllNan}


class _FeaturizersType:
    """Names for featurizer factory types"""
    Numeric = 'numeric'
    DateTime = 'datetime'
    Categorical = 'categorical'
    Text = 'text'
    Generic = 'generic'


class SupportedTransformers:
    """Customer Facing Names for transformers supported by AutoML."""

    # Generic
    ImputationMarker = 'ImputationMarker'
    Imputer = 'Imputer'
    MaxAbsScaler = 'MaxAbsScaler'

    # Categorical
    CatImputer = 'CatImputer'
    HashOneHotEncoder = 'HashOneHotEncoder'
    LabelEncoder = 'LabelEncoder'
    CatTargetEncoder = 'CatTargetEncoder'
    WoETargetEncoder = 'WoETargetEncoder'
    OneHotEncoder = 'OneHotEncoder'

    # DateTime
    DateTimeTransformer = 'DateTimeTransformer'

    # Text
    CountVectorizer = 'CountVectorizer'
    NaiveBayes = 'NaiveBayes'
    StringCast = 'StringCast'
    TextTargetEncoder = 'TextTargetEncoder'
    TfIdf = 'TfIdf'
    WordEmbedding = 'WordEmbedding'

    CUSTOMIZABLE_TRANSFORMERS = {
        HashOneHotEncoder,
        Imputer,
        TfIdf
    }

    BLOCK_TRANSFORMERS = {
        HashOneHotEncoder,
        LabelEncoder,
        CatTargetEncoder,
        WoETargetEncoder,
        OneHotEncoder,
        CountVectorizer,
        NaiveBayes,
        TextTargetEncoder,
        TfIdf,
        WordEmbedding
    }

    FULL_SET = {
        ImputationMarker,
        Imputer,
        MaxAbsScaler,
        CatImputer,
        HashOneHotEncoder,
        LabelEncoder,
        CatTargetEncoder,
        WoETargetEncoder,
        OneHotEncoder,
        DateTimeTransformer,
        CountVectorizer,
        NaiveBayes,
        StringCast,
        TextTargetEncoder,
        TfIdf,
        WordEmbedding
    }


class TransformerParams:
    """Parameters used by all transformers in AutoML."""

    class Imputer:
        """Parameters used by all transformers in AutoML."""
        Strategy = "strategy"
        Constant = "constant"
        Mean = "mean"
        Median = "median"
        Mode = "most_frequent"
        FillValue = "fill_value"
        # Forecasting tasks specific parameters.
        ForecastingEnabledStrategies = {Mean, Median, Mode, Constant}
        ForecastingTargetEnabledStrategies = {Constant}

    class Nimbus:
        """Parameters used by nimbus in AutoML."""
        Mean = 'Mean'
        Min = 'Minimum'
        Max = 'Maximum'
        DefaultValue = 'DefaultValue'


class SupportedTransformersInternal(SupportedTransformers):
    """Transformer Names for all transformers supported by AutoML, including those not exposed."""

    # Generic
    LambdaTransformer = 'LambdaTransformer'
    MiniBatchKMeans = 'MiniBatchKMeans'

    # Numeric
    BinTransformer = 'BinTransformer'

    # Text
    BagOfWordsTransformer = 'BagOfWordsTransformer'
    StringConcat = 'StringConcat'
    TextStats = 'TextStats'
    AveragedPerceptronTextTargetEncoder = 'AveragedPerceptronTextTargetEncoder'

    # TimeSeries
    GrainMarker = 'GrainMarker'
    MaxHorizonFeaturizer = 'MaxHorizonFeaturizer'
    Lag = 'Lag'
    RollingWindow = 'RollingWindow'
    STLFeaturizer = 'STLFeaturizer'

    # Ignore
    Drop = ''

    FULL_SET = {
        LambdaTransformer,
        MiniBatchKMeans,
        BinTransformer,
        BagOfWordsTransformer,
        StringConcat,
        TextStats,
        AveragedPerceptronTextTargetEncoder,
        GrainMarker,
        MaxHorizonFeaturizer,
        Lag,
        RollingWindow,
        STLFeaturizer,
        Drop
    }.union(set(SupportedTransformers.FULL_SET))


class SupportedTransformersFactoryNames:
    """Method names for transformers. This is Featurizers factory method names."""

    class Generic:
        """Supported transformer factory method for generic type data."""

        ImputationMarker = 'imputation_marker'
        LambdaTransformer = 'lambda_featurizer'
        Imputer = 'imputer'
        MiniBatchKMeans = 'minibatchkmeans_featurizer'
        MaxAbsScaler = 'maxabsscaler'

    class Numeric:
        """Supported transformer factory method for numeric type data."""

        BinTransformer = 'bin_transformer'

    class Categorical:
        """Supported transformer factory method for categorical type data."""

        CatImputer = 'cat_imputer'
        HashOneHotVectorizerTransformer = 'hashonehot_vectorizer'
        LabelEncoderTransformer = 'labelencoder'
        CatTargetEncoder = 'cat_targetencoder'
        WoEBasedTargetEncoder = 'woe_targetencoder'
        OneHotEncoderTransformer = 'onehotencoder'

    class DateTime:
        """Supported transformer factory method for datetime type data."""

        DateTimeFeaturesTransformer = 'datetime_transformer'

    class Text:
        """Supported transformer factory method for text type data."""

        BagOfWordsTransformer = 'bow_transformer'
        CountVectorizer = 'count_vectorizer'
        NaiveBayes = 'naive_bayes'
        StringCastTransformer = 'string_cast'
        StringConcatTransformer = 'string_concat'
        StatsTransformer = 'text_stats'
        TextTargetEncoder = 'text_target_encoder'
        AveragedPerceptronTextTargetEncoder = 'averaged_perceptron_text_target_encoder'
        TfidfVectorizer = 'tfidf_vectorizer'
        WordEmbeddingTransformer = 'word_embeddings'


class TransformerName:
    """Transformer names with customer and factory method names."""

    def __init__(self, customer_transformer_name, transformer_method_name):
        """Init TransformerName."""
        self.customer_transformer_name = customer_transformer_name
        self.transformer_method_name = transformer_method_name


class SupportedTransformerNames:
    """A list of supported transformers with all customer name and factory method name."""

    SupportedGenericTransformerList = [
        TransformerName(
            SupportedTransformersInternal.ImputationMarker,
            SupportedTransformersFactoryNames.Generic.ImputationMarker
        ),
        TransformerName(
            SupportedTransformersInternal.LambdaTransformer,
            SupportedTransformersFactoryNames.Generic.LambdaTransformer
        ),
        TransformerName(
            SupportedTransformersInternal.Imputer,
            SupportedTransformersFactoryNames.Generic.Imputer
        ),
        TransformerName(
            SupportedTransformersInternal.MiniBatchKMeans,
            SupportedTransformersFactoryNames.Generic.MiniBatchKMeans
        ),
        TransformerName(
            SupportedTransformersInternal.MaxAbsScaler,
            SupportedTransformersFactoryNames.Generic.MaxAbsScaler
        ),
    ]

    SupportedNumericTransformerList = [
        TransformerName(
            SupportedTransformersInternal.BinTransformer,
            SupportedTransformersFactoryNames.Numeric.BinTransformer
        )
    ]

    SupportedCategoricalTransformerList = [
        TransformerName(
            SupportedTransformersInternal.CatImputer,
            SupportedTransformersFactoryNames.Categorical.CatImputer
        ),
        TransformerName(
            SupportedTransformersInternal.HashOneHotEncoder,
            SupportedTransformersFactoryNames.Categorical.HashOneHotVectorizerTransformer
        ),
        TransformerName(
            SupportedTransformersInternal.LabelEncoder,
            SupportedTransformersFactoryNames.Categorical.LabelEncoderTransformer
        ),
        TransformerName(
            SupportedTransformersInternal.CatTargetEncoder,
            SupportedTransformersFactoryNames.Categorical.CatTargetEncoder
        ),
        TransformerName(
            SupportedTransformersInternal.WoETargetEncoder,
            SupportedTransformersFactoryNames.Categorical.WoEBasedTargetEncoder
        ),
        TransformerName(
            SupportedTransformersInternal.OneHotEncoder,
            SupportedTransformersFactoryNames.Categorical.OneHotEncoderTransformer)
    ]

    SupportedDateTimeTransformerList = [
        TransformerName(
            SupportedTransformersInternal.DateTimeTransformer,
            SupportedTransformersFactoryNames.DateTime.DateTimeFeaturesTransformer
        )
    ]

    SupportedTextTransformerList = [
        TransformerName(
            SupportedTransformersInternal.BagOfWordsTransformer,
            SupportedTransformersFactoryNames.Text.BagOfWordsTransformer
        ),
        TransformerName(
            SupportedTransformersInternal.CountVectorizer,
            SupportedTransformersFactoryNames.Text.CountVectorizer
        ),
        TransformerName(
            SupportedTransformersInternal.NaiveBayes,
            SupportedTransformersFactoryNames.Text.NaiveBayes
        ),
        TransformerName(
            SupportedTransformersInternal.StringCast,
            SupportedTransformersFactoryNames.Text.StringCastTransformer
        ),
        TransformerName(
            SupportedTransformersInternal.StringConcat,
            SupportedTransformersFactoryNames.Text.StringConcatTransformer
        ),
        TransformerName(
            SupportedTransformersInternal.TextStats,
            SupportedTransformersFactoryNames.Text.StatsTransformer
        ),
        TransformerName(
            SupportedTransformersInternal.TextTargetEncoder,
            SupportedTransformersFactoryNames.Text.TextTargetEncoder
        ),
        TransformerName(
            SupportedTransformersInternal.TfIdf,
            SupportedTransformersFactoryNames.Text.TfidfVectorizer
        ),
        TransformerName(
            SupportedTransformersInternal.AveragedPerceptronTextTargetEncoder,
            SupportedTransformersFactoryNames.Text.AveragedPerceptronTextTargetEncoder
        ),
        TransformerName(
            SupportedTransformersInternal.WordEmbedding,
            SupportedTransformersFactoryNames.Text.WordEmbeddingTransformer
        )
    ]


class TransformerNameMappings:
    """Transformer name mappings."""

    CustomerFacingTransformerToTransformerMapGenericType = dict(zip(
        [transformer.customer_transformer_name for transformer
         in SupportedTransformerNames.SupportedGenericTransformerList],
        [transformer.transformer_method_name for transformer
         in SupportedTransformerNames.SupportedGenericTransformerList]))

    CustomerFacingTransformerToTransformerMapCategoricalType = dict(zip(
        [transformer.customer_transformer_name for transformer
         in SupportedTransformerNames.SupportedCategoricalTransformerList],
        [transformer.transformer_method_name for transformer
         in SupportedTransformerNames.SupportedCategoricalTransformerList]))

    CustomerFacingTransformerToTransformerMapNumericType = dict(zip(
        [transformer.customer_transformer_name for transformer
         in SupportedTransformerNames.SupportedNumericTransformerList],
        [transformer.transformer_method_name for transformer
         in SupportedTransformerNames.SupportedNumericTransformerList]))

    CustomerFacingTransformerToTransformerMapDateTimeType = dict(zip(
        [transformer.customer_transformer_name for transformer
         in SupportedTransformerNames.SupportedDateTimeTransformerList],
        [transformer.transformer_method_name for transformer
         in SupportedTransformerNames.SupportedDateTimeTransformerList]))

    CustomerFacingTransformerToTransformerMapText = dict(zip(
        [transformer.customer_transformer_name for transformer
         in SupportedTransformerNames.SupportedTextTransformerList],
        [transformer.transformer_method_name for transformer
         in SupportedTransformerNames.SupportedTextTransformerList]))


class TextNeuralNetworks:
    """Names of neural models swept for text classification."""

    # feature sweeping config names
    BILSTM = "BiLSTMTextEmbeddings"
    BERT = "PreTrainedDNNEmbeddings"
    ALL = [BILSTM, BERT]

    # class names
    BILSTM_CLASS_NAME = "BiLSTMAttentionTransformer"
    BERT_CLASS_NAME = "PretrainedTextDNNTransformer"
    ALL_CLASS_NAMES = [BILSTM_CLASS_NAME, BERT_CLASS_NAME]


class _OperatorNames:
    """Class storing operator names for various transformations."""

    CharGram = 'CharGram'
    WordGram = 'WordGram'
    Mean = 'Mean'
    Mode = 'Mode'
    Median = 'Median'
    Constant = 'Constant'
    Min = 'Min'
    Max = 'Max'
    DefaultValue = 'DefaultValue'

    FULL_SET = {CharGram, WordGram, Mean, Mode, Median, Min, Max, Constant, DefaultValue}


class _TransformerOperatorMappings:
    Imputer = {
        TransformerParams.Imputer.Mean: _OperatorNames.Mean,
        TransformerParams.Imputer.Mode: _OperatorNames.Mode,
        TransformerParams.Imputer.Median: _OperatorNames.Median,
        TransformerParams.Imputer.Constant: _OperatorNames.Constant
    }
    NimbusImputer = {
        TransformerParams.Nimbus.Mean: _OperatorNames.Mean,
        TransformerParams.Nimbus.Min: _OperatorNames.Min,
        TransformerParams.Nimbus.Max: _OperatorNames.Max,
        TransformerParams.Nimbus.DefaultValue: _OperatorNames.DefaultValue
    }


class SweepingMode:
    """Sweeping mode names"""

    Feature = 'feature'
    Balancing = 'balancing'
