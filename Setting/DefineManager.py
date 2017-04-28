# Use These Various From ProgramMain.py
USE_OPENCV_VERSION = "3.2.0"
OBJECT_DETECT_TESTCASE_PATH = "Tests/testcase8/"
FIND_CORNER_TESTCASE_PATH = "Tests/testcase7/"
TESTCASE_BEFORE_IMAGE_PATH = OBJECT_DETECT_TESTCASE_PATH + "before.jpg"
TESTCASE_AFTER_IMAGE_PATH = OBJECT_DETECT_TESTCASE_PATH + "after.jpg"

# Use These Various From ObjectDetect.py
MORPHOLOGY_MASK_SIZE = 5        #Use Odd Number
BLUR_MASK_SIZE = 3
EACH_IMAGE_DIFFERENCE_THRESHOLD = 30
SET_IMAGE_WHITE_COLOR = 255
SET_IMAGE_BLACK_COLOR = 0
NEIGHBORHOOD_MASK_SIZE = 7
CANNY_MINIMUM_THRESHOLD = 100
CANNY_MAXIMUM_THRESHOLD = 150
GET_MAXIMUM_AREA_SIZE = 5
SQUARE_CORNER_NUM = 4
IMAGE_WIDTH = 292.0
RGB_COLOR_BLACK = (0,0,0)
RGB_COLOR_BLUE = (255,0,0)
RGB_COLOR_GREEN = (0,255,0)
RGB_COLOR_RED = (0,0,255)
RGB_COLOR_WHITE = (255,255,255)

# Use These Various From LogManager.py
LOG_LEVEL_DEBUG = 0
LOG_LEVEL_INFO = 1
LOG_LEVEL_WARN = 2
LOG_LEVEL_ERROR = 3

# Use These Various From GetContour.py
RESEARCH_ANGLE_COUNT = 125
GOLDEN_RATIO = 1.61803398875
MINIMUM_STRIDE_KEY = 7
ANGLE_AS_DEAL_WITH_POINT =15
BASE_MEAN = 128.147325937           #From Tests/testcase5
BASE_DEVIATION = 73.6300617744
SQUARE_LENGTH_MEAN = 30.2072184969  #From Tests/testcase5
RADIAN_TO_DEGREE = 180.0 / 3.14159265358979323846264338327950288
SIMILAR_RATE = 0.95
MINIMUM_RECT_AREA_SIZE = 900
K = 7
SIGMA = 17
ALPHA = 2.4
BETA = -1.73
THRESHOLD= 150
WIDTH_MASK_SIZE = 23
HEIGHT_MASK_SIZE = 57
ADD_IMAGE_WIDTH = 11
ADD_IMAGE_HEIGHT = 23
END_CONTOUR_COUNT = 4