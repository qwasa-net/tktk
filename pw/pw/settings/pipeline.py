PIPELINE = {

    # if assets should be processed
    'PIPELINE_ENABLED': True,

    # if assets should be collected in develop
    'PIPELINE_COLLECTOR_ENABLED': False,

    'JAVASCRIPT': {

        'vuebase': {
            'source_filenames': (
                'scripts/libs/vue.min.js',
                'scripts/libs/axios.min.js',
            ),
            'output_filename': 'libs.js',
            'extra_context': {
                'defer': False,
                'async': False
            },
        },

        'tktk': {
            'source_filenames': (
                'scripts/soundman.js',
                'scripts/components.js',
                'scripts/k4bg.js',
                'scripts/k4bg_auto.js',
                'tktk/tktk.js',
            ),
            'output_filename': 'tktk/script.js',
            'extra_context': {
                'defer': False,
                'async': False
            },
        },

        'index': {
            'source_filenames': (
                'scripts/hello.js',
                'scripts/k3bg.js',
                'scripts/k3bg_auto.js',
                'index/index.js',
            ),
            'output_filename': 'index/script.js',
            'extra_context': {
                'defer': False,
                'async': False
            },
        },

    },

    'STYLESHEETS': {

        'tktk': {
            'source_filenames': (
                'styla/style.less',
                'styla/components.less',
                'styla/k3bg.css',
                'tktk/tktk.less',
            ),
            'output_filename': 'tktk/style.css',
        },

        'index': {
            'source_filenames': (
                'styla/style.less',
                'index/index.less',
                'styla/k3bg.css',
            ),
            'output_filename': 'index/style.css',
        },

    },

    'COMPILERS': ('pipeline.compilers.less.LessCompiler',),
    'LESS_BINARY': '/usr/bin/lessc',
    'LESS_ARGUMENTS': '--no-js -x --include-path="../../../../static/styla"',

    'CSS_COMPRESSOR': 'pipeline.compressors.NoopCompressor',
    'JS_COMPRESSOR': 'pipeline.compressors.NoopCompressor',
    # 'JS_COMPRESSOR': 'pipeline.compressors.uglifyjs.UglifyJSCompressor',
    # 'CSS_COMPRESSOR': 'pipeline.compressors.yuglify.YuglifyCompressor',

}
