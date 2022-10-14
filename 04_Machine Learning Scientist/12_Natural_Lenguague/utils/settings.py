import os

# Formatos Depurado (Debugging)
ERROR_FORMAT = "%(levelname)s at %(asctime)s in %(funcName)s in %(filename) at line %(lineno)d: %(message)s"
DEBUG_FORMAT = '%(asctime)s [%(levelname)s] %(name)s: %(message)s'

# Carpetas (Folders)
ROOT_FOLDER = 'django_api/api_data'
SCRIPTS_FOLDER = os.path.join(ROOT_FOLDER, 'scripts/')
CONFIG_FOLDER = os.path.join(ROOT_FOLDER, 'config/')
LOG_FOLDER = os.path.join(ROOT_FOLDER, 'log/')
MODELS_FOLDER = os.path.join(ROOT_FOLDER, 'models/')
DATA_FOLDER = os.path.join(ROOT_FOLDER, 'data/')
PLOTS_FOLDER = os.path.join(ROOT_FOLDER, 'plots/')
PARAMS_FOLDER = os.path.join(ROOT_FOLDER, 'params/')
TRACE_FOLDER = os.path.join(ROOT_FOLDER, 'trace/')

_DATA_MODELS_FOLDER = \
    os.path.join(DATA_FOLDER, 'models/')
_RAW_DATA_FOLDER = \
    os.path.join(DATA_FOLDER, 'raw/')

# Runtype
RUN_TYPE = 'production'
RUN_TYPE_FOLDER = 'prod/'

# Flask settings
FLASK_SERVER_NAME = 'localhost:80'
FLASK_DEBUG = True  # Do not use debug mode in production

# Flask-Restplus settings
RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False
RESTPLUS_ERROR_404_HELP = False

# Nombres de Archivos
_EVENTOS_FILE = "eventos_documents.gzip"# Nombre archivo eventos documentos
_L2R_FILE = 'model_l2r.json'            # Nombre archivo del modelo l2r
_SIM_MATRIX_FILE = "word2vec_.index"    # Nombre archivo matriz de similaridad
_W2V_FILE = "model_w2v.model"           # Nombre archivo del modelo w2v

# Rutas a cargar en función load
EVENTOS_DATA = \
    os.path.join(_RAW_DATA_FOLDER, _EVENTOS_FILE)

MODEL_W2V = \
    os.path.join(_DATA_MODELS_FOLDER, 'w2v/', _W2V_FILE)

MODEL_SIM_MATRIX = \
    os.path.join(_DATA_MODELS_FOLDER, 'index/', _SIM_MATRIX_FILE)

MODEL_GMM_MEANS = \
    os.path.join(_DATA_MODELS_FOLDER, 'gmm/', "means.npy")
MODEL_GMM_COVARS = \
    os.path.join(_DATA_MODELS_FOLDER, 'gmm/', "covariances.npy")
MODEL_GMM_WEIGHTS = \
    os.path.join(_DATA_MODELS_FOLDER, 'gmm/', "weights.npy")

# Rutas de salida sim_matrix
OUTPUT_SIM_MATRIX = \
    os.path.join(_DATA_MODELS_FOLDER, 'index/')

# Variables Búsqueda de Rangos
COUNTRIES = ['AR', 'MX']
EVENT_TYPES = ["A", "D", "I"]
RISKS = ["ALTO", "BAJO", "MEDIO", ""]
NATURE = ["A", "H", "S"]
GRAVITY = ["1", "2", "3", "4", " "]

# - REVISAR:  Modificar índices cuando se modifique la estructura de datos
# Glosario eventos_documents.gzip (al 29/04/2022)
# Data columns (total 16 columns):
gev = \
    {
        'C_EVENTO': 0,              # int64
        'C_TIPO_RIESGO': 1,         # float64
        'ID_FACTOR': 2,             # float64
        'C_ESTRUCTURA': 3,          # int64
        'NRO_EVENTO': 4,            # object
        'I_TIPO_EVENTO': 5,         # object
        'D_RIESGO_POTENCIAL': 6,    # object
        'I_GRAVEDAD': 7,            # object
        'I_PROBABILIDAD': 8,        # object
        'D_EVENTO': 9,              # object
        'fecha_ocurrencia': 10,     # datetime64[ns]
        'IDPAIS': 11,               # object
        'ID_PLANTA': 12,            # float64
        'gaussian': 13,             # int64
        'I_NATURALEZA': 14,         # object
        'level_0': 15,              # int64
    }

# Utilizado en funciones de feedback en W2VCluster
SIMILITUD_MINIMA_ENTRE_CONSULTAS = 0.7
FEEDBACK_DATA = \
    os.path.join(_RAW_DATA_FOLDER, 'búsquedas_local (6).parquet')


# Learning to Rank
MODEL_L2R = \
    os.path.join(_DATA_MODELS_FOLDER, 'l2r/',_L2R_FILE)
