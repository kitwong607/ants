from .future_strategy import FutureAbstractStrategy
from ..order.base import OrderAction, OrderType
#from ..order.ib_order import IBMktOrder
from .. import utilities
from ..session import SessionMode

from ..ta.Range import *
from ..signal import entry
from ..signal import exit

class LongSignalTesterOrderedAPM5T(FutureAbstractStrategy):
    IS_DISPLAY_IN_OPTION = True
    OPTIMIZATION_PAIR = []
    #SELECTED_SIGNAL = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335, 336, 337, 338, 339, 340, 341, 342, 343, 344, 345, 346, 347, 348, 349, 350, 351, 352, 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477, 478, 479, 480, 481, 482, 483, 484, 485, 486, 487, 488, 489, 490, 491, 492, 493, 494, 495, 496, 497, 498, 499, 500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 512, 513, 514, 515, 516, 517, 518, 519, 520, 521, 522, 523, 524, 525, 526, 527, 528, 529, 530, 531, 532, 533, 534, 535, 536, 537, 538, 539, 540, 541, 542, 543, 544, 545, 546, 547, 548, 549, 550, 551, 552, 553, 554, 555, 556, 557, 558, 559, 560, 561, 562, 563, 564, 565, 566, 567, 568, 569, 570, 571, 572, 573, 574, 575, 576, 577, 578, 579, 580, 581, 582, 583, 584, 585, 586, 587, 588, 589, 590, 591, 592, 593, 594, 595, 596, 597, 598, 599, 600, 601, 602, 603, 604, 605, 606, 607, 608, 609, 610, 611, 612, 613, 614, 615, 616, 617, 618, 619, 620, 621, 622, 623, 624, 625, 626, 627, 628, 629, 630, 631, 632, 633, 634, 635, 636, 637, 638, 639, 640, 641, 642, 643, 644, 645, 646, 647, 648, 649, 650, 651, 652, 653, 654, 655, 656, 657, 658, 659, 660, 661, 662, 663, 664, 665, 666, 667, 668, 669, 670, 671, 672, 673, 674, 675, 676, 677, 678, 679, 680, 681, 682, 683, 684, 685, 686, 687, 688, 689, 690, 691, 692, 693, 694, 695, 696, 697, 698, 699, 700, 701, 702, 703, 704, 705, 706, 707, 708, 709, 710, 711, 712, 713, 714, 715, 716, 717, 718, 719, 720, 721, 722, 723, 724, 725, 726, 727, 728, 729, 730, 731, 732, 733, 734, 735, 736, 737, 738, 739, 740, 741, 742, 743, 744, 745, 746, 747, 748, 749, 750, 751, 752, 753, 754, 755, 756, 757, 758, 759, 760, 761, 762, 763, 764, 765, 766, 767, 768, 769, 770, 771, 772, 773, 774, 775, 776, 777, 778, 779, 780, 781, 782, 783, 784, 785, 786, 787, 788, 789, 790, 791, 792, 793, 794, 795, 796, 797, 798, 799, 800, 801, 802, 803, 804, 805, 806, 807, 808, 809, 810, 811, 812, 813, 814, 815, 816, 817, 818, 819, 820, 821, 822, 823, 824, 825, 826, 827, 828, 829, 830, 831, 832, 833, 834, 835, 836, 837, 838, 839, 840, 841, 842, 843, 844, 845, 846, 847, 848, 849, 850, 851, 852, 853, 854, 855, 856, 857, 858, 859, 860, 861, 862, 863, 864, 865, 866, 867, 868, 869, 870, 871, 872, 873, 874, 875, 876, 877, 878, 879, 880, 881, 882, 883, 884, 885, 886]
    #SELECTED_SIGNAL = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335, 336, 337, 338, 339, 340, 341, 342, 343, 344, 345, 346, 347, 348, 349, 350, 351, 352, 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477, 478, 479, 480, 481, 482, 483, 484, 485, 486, 487, 488, 489, 490, 491, 492, 493, 494, 495, 496, 497, 498, 499, 500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 512, 513, 514, 515, 516, 517, 518, 519, 520, 521, 522, 523, 524, 525, 526, 527, 528, 529, 530, 531, 532, 533, 534, 535, 536, 537, 538, 539, 540, 541, 542, 543, 544, 545, 546, 547, 548, 549, 550, 551, 552, 553, 554, 555, 556, 557, 558, 559, 560, 561, 562, 563, 564, 565, 566, 567, 568, 569, 570, 571, 572, 573, 574, 575, 576, 577, 578, 579, 580, 581, 582, 583, 584, 585, 586, 587, 588, 589, 590, 591, 592, 593, 594, 595, 596, 597, 598, 599, 600, 601, 602, 603, 604, 605, 606, 607, 608, 609, 610, 611, 612, 613, 614, 615, 616, 617, 618, 619, 620, 621, 622, 623, 624, 625, 626, 627, 628, 629, 630, 631, 632, 633, 634, 635, 636, 637, 638, 639, 640, 641, 642, 643, 644, 645, 646, 647, 648, 649, 650, 651, 652, 653, 654, 655, 656, 657, 658, 659, 660, 661, 662, 663, 664, 665, 666, 667, 668, 669, 670, 671, 672, 673, 674, 675, 676, 677, 678, 679, 680, 681, 682, 683, 684, 685, 686, 687, 688, 689, 690, 691, 692, 693, 694, 695, 696, 697, 698, 699, 700, 701, 702, 703, 704, 705, 706, 707, 708, 709, 710, 711, 712, 713, 714, 715, 716, 717, 718, 719, 720, 721, 722, 723, 724, 725, 726, 727, 728, 729, 730, 731, 732, 733, 734, 735, 736, 737, 738, 739, 740, 741, 742, 743, 744, 745, 746, 747, 748, 749, 750, 751, 752, 753, 754, 755, 756, 757, 758, 759, 760, 761, 762, 763, 764, 765, 766, 767, 768, 769, 770, 771, 772, 773, 774, 775, 776, 777, 778, 779, 780, 781, 782, 783, 784, 785, 786, 787, 788, 789, 790, 791, 792, 793, 794, 795, 796, 797, 798, 799, 800, 801, 802, 803, 804, 805, 806, 807, 808, 809, 810, 811, 812, 813, 814, 815, 816, 817, 818, 819, 820, 821, 822, 823, 824, 825, 826, 827, 828, 829, 830, 831, 832, 833, 834, 835, 836, 837, 838, 839, 840, 841, 842, 843, 844, 845, 846, 847, 848, 849, 850, 851, 852, 853, 854, 855, 856, 857, 858, 859, 860, 861, 862, 863, 864, 865, 866, 867, 868, 869, 870, 871, 872, 873, 874, 875, 876, 877, 878, 879, 880, 881, 882, 883, 884, 885, 886, 887, 888, 889, 890, 891, 892, 893, 894, 895, 896, 897, 898, 899, 900, 901, 902, 903, 904, 905, 906, 907, 908, 909, 910, 911, 912, 913, 914, 915, 916]

    '''
    #For time period
    backtestPeriod = [[[2016, 1], [2016, 6]], [[2016, 7], [2016, 12]],
                      [[2017, 1], [2017, 6]], [[2017, 7], [2017, 12]],
                      [[2018, 1], [2018, 6]], [[2018, 7], [2018, 12]]]
    
    #SELECTED_SIGNAL = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 74, 76, 77, 79, 80, 81, 82, 83, 85, 86, 88, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 233, 234, 235, 236, 237, 243, 244, 245, 246, 247, 248, 250, 251, 252, 253, 254, 255, 256, 258, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 276, 279, 282, 285, 288, 289, 291, 293, 294, 297, 299, 300, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 317, 320, 321, 323, 325, 327, 328, 329, 330, 331, 332, 341, 345, 346, 349, 351, 352, 353, 359, 361, 364, 365, 368, 369, 373, 375, 378, 392, 393, 394, 396, 398, 412, 419, 421, 425, 428, 429, 433, 434, 435, 436, 437, 439, 440, 442, 443, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 471, 474, 477, 478, 482, 483, 486, 487, 488, 490, 491, 492, 493, 494, 496, 497, 500, 503, 507, 510, 511, 512, 513, 515, 516, 518, 519, 522, 527, 532, 533, 534, 540, 542, 543, 545, 546, 547, 548, 549, 550, 556, 557, 558, 559, 560, 561, 566, 567, 568, 569, 571, 572, 573, 576, 577, 579, 581, 584, 585, 587, 588, 589, 591, 592, 593, 595, 598, 600, 601, 603, 607, 611, 614, 618, 625, 626, 627, 629, 632, 633, 642, 644, 646, 649, 650, 653, 654, 656, 658, 666, 672, 673, 674, 676, 677, 681, 686, 687, 690, 691, 694, 695, 696, 698, 700, 701, 704, 705, 710, 711, 714, 715, 718, 719, 720, 721, 722, 724, 725, 734, 735, 739, 742, 743, 744, 746, 753, 754, 755, 758, 759, 763, 764, 765, 766, 767, 770, 771, 774, 775, 777, 778, 779, 781, 782, 783, 784, 785, 786, 787, 788, 789, 792, 795, 797, 798, 799, 801, 804, 805, 807, 808, 809, 810, 811, 812, 813, 814, 817, 821, 823, 825, 826, 827, 828, 829, 830, 831, 832, 833, 837, 838, 840, 841, 842, 843, 844, 847, 877, 878, 880, 881, 882, 884, 885, 886]
    '''

    '''
    #For time period
    backtestPeriod = [[[2017, 1], [2017, 6]], [[2018, 11], [2019, 4]]]
    
    SELECTED_SIGNAL = [3, 10, 37, 38, 52, 53, 54, 70, 74, 76, 77, 79, 80, 82, 83, 85, 86, 88, 90, 91, 93, 95, 96, 170, 174, 178, 179, 194,
     205, 206, 208, 209, 220, 231, 233, 234, 235, 236, 237, 244, 245, 250, 251, 253, 254, 256, 258, 261, 262, 264, 265,
     266, 267, 268, 271, 272, 273, 306, 308, 309, 310, 311, 313, 314, 317, 320, 321, 325, 329, 332, 341, 345, 393, 412,
     429, 436, 437, 440, 443, 446, 447, 450, 453, 454, 456, 457, 458, 459, 460, 462, 463, 466, 478, 482, 483, 486, 487,
     490, 491, 492, 493, 494, 496, 497, 507, 510, 511, 512, 515, 518, 532, 533, 542, 543, 545, 556, 557, 558, 568, 569,
     571, 577, 579, 585, 587, 588, 589, 593, 603, 618, 625, 629, 656, 676, 677, 691, 695, 700, 701, 704, 705, 715, 719,
     721, 722, 735, 739, 742, 744, 746, 753, 754, 755, 759, 770, 774, 775, 777, 778, 779, 789, 797, 798, 801, 804, 807,
     808, 810, 811, 812, 821, 825, 826, 827, 828, 830, 837, 838, 840, 841, 842, 843, 847, 881, 886]
    '''

    '''
    #For time period
    backtestPeriod = [[[2016, 6], [2016, 11]], [[2016, 12], [2017, 5]],
                      [[2017, 6], [2017, 11]], [[2017, 12], [2018, 5]],
                      [[2018, 6], [2018, 11]], [[2018, 12], [2019, 5]]]
    '''
    SELECTED_SIGNAL = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 66, 67, 68, 69, 70, 73, 74, 76, 77, 79, 80, 82, 83, 85, 86, 88, 90, 91, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 107, 108, 109, 110, 111, 112, 113, 114, 118, 120, 121, 122, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 139, 140, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 171, 172, 173, 175, 176, 177, 178, 179, 183, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 202, 203, 205, 206, 207, 208, 209, 210, 213, 214, 215, 216, 217, 218, 219, 220, 221, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 239, 241, 242, 244, 245, 247, 248, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 276, 277, 279, 282, 285, 286, 287, 288, 289, 291, 292, 294, 297, 300, 301, 302, 303, 305, 306, 307, 308, 309, 310, 311, 312, 315, 317, 318, 320, 321, 322, 323, 324, 325, 327, 328, 329, 330, 332, 333, 335, 338, 354, 358, 363, 364, 373, 376, 381, 385, 388, 389, 391, 392, 396, 397, 401, 405, 407, 408, 409, 411, 412, 413, 415, 423, 433, 434, 436, 437, 438, 439, 441, 442, 443, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 471, 472, 474, 475, 478, 482, 483, 486, 487, 488, 490, 491, 492, 493, 494, 495, 496, 497, 498, 499, 500, 501, 503, 504, 505, 507, 508, 509, 510, 511, 512, 515, 517, 518, 520, 521, 530, 531, 532, 533, 534, 535, 536, 539, 542, 544, 549, 550, 551, 552, 553, 554, 555, 556, 557, 558, 561, 562, 563, 564, 565, 566, 567, 568, 569, 572, 573, 575, 576, 577, 581, 582, 584, 585, 587, 588, 589, 591, 592, 593, 594, 595, 596, 597, 599, 600, 601, 603, 611, 612, 613, 614, 618, 621, 622, 626, 627, 628, 632, 635, 640, 641, 642, 648, 651, 652, 653, 655, 656, 659, 661, 662, 665, 667, 668, 669, 672, 673, 674, 675, 677, 679, 680, 681, 687, 689, 691, 695, 696, 697, 698, 700, 701, 703, 704, 705, 706, 707, 710, 711, 715, 716, 717, 719, 720, 721, 722, 723, 727, 729, 734, 735, 740, 742, 744, 745, 746, 747, 749, 750, 751, 755, 756, 759, 767, 768, 769, 770, 771, 772, 773, 774, 775, 776, 777, 778, 779, 781, 782, 783, 784, 785, 786, 787, 788, 789, 790, 792, 793, 794, 797, 798, 801, 804, 805, 806, 807, 808, 809, 810, 811, 812, 813, 814, 815, 817, 818, 819, 820, 821, 822, 823, 824, 825, 826, 827, 828, 829, 830, 831, 832, 833, 837, 838, 840, 842, 847, 849, 850, 877, 878, 881, 882, 883, 884, 885, 886, 888, 889, 890, 892, 893, 894, 896, 897, 898, 906, 908, 909, 910, 911, 913, 915, 916]




    '''
    SELECTED_SIGNAL = [
                        # 1 Breakout previous day high
                        # 2 Breakout previous day high with delay
                        # 3 Breakout previous day high with delay and maintain breakout
                        # 4 Breakout previous high
                        # 5 Breakout previous high with delay
                        # 6 Breakout previous high with delay and maintain breakout
                        # 7 Breakout previous day open
                        # 8 Breakout previous day open with delay
                        # 9 Breakout previous day open with delay and maintain breakout
                        # 10 Breakout previous day close
                        # 11 Breakout previous day close with delay
                        # 12 Breakout previous day close with delay and maintain breakout
                        # 13 Breakout previous low
                        # 14 Breakout previous low with delay
                        # 15 Breakout previous low with delay and maintain breakout
                        # 16 Daily higher high
                        # 17 Previous day daily higher high
                        # 18 Daily higher low
                        # 19 Previous day daily higher low
                        # 20 Daily lower high
                        # 21 Previous day daily lower high
                        # 22 Daily lower low
                        # 23 Previous day daily lower low
                        # 24 Intra day higher high
                        # 25 Intra day higher high with delay
                        # 26 Intra day higher low
                        # 27 Intra day higher low with delay
                        # 28 Intra day lower high
                        # 29 Intra day lower high with delay
                        # 30 Intra day lower low
                        # 31 Intra day lower low with delay
                        # 32 Intra day higher high and higer low
                        # 33 Intra day higher high and higer low with delay
                        # 34 Day open inside pivot point zone
                        # 35 Close inside pivot point zone
                        # 36 Min RSI Higher threshold related
                        # 37 Min RSI Higher threshold related with delay
                        # 38 Min RSI Higher threshold related with delay and maintain threshold level
                        # 39 Min RSI Higher threshold related with delay and cannot maintain threshold level
                        # 40 Max RSI Lower threshold related
                        # 41 Max RSI Lower threshold related with delay
                        # 42 Max RSI Lower threshold related with delay and maintain threshold level
                        # 43 Max RSI Lower threshold related with delay and cannot maintain threshold level
                        # 44 close higher SMA related
                        # 45 close higher SMA related with delay
                        # 46 close higher SMA related with delay and maintain breakout
                        # 47 close SMA cross
                        # 48 Close Higher Morning OHLC
                        # 49 Close Higher Morning OHLC with delay
                        # 50 Close Higher Morning OHLC with delay and maintain breakout
                        # 51 Intra day MACD cross
                        # 52 Intra day MACD cross with delay
                        # 53 Inter day MACD cross
                        # 54 Intra day Stochastic cross
                        # 55 Intra day Stochastic cross with delay
                        # 56 Inter day Stochastic cross
                        # 57 Intra day Stochastic Fast cross
                        # 58 Intra day Stochastic Fast cross with delay and maintain
                        # 59 Inter day Stochastic Fast cross
                        # 60 Intra day Stochastic Relative Strength Index cross
                        # 61 Intra day Stochastic Relative Strength Index cross with delay and maintain
                        # 62 Inter day Stochastic Relative Strength Index cross
                        # 63 Intra day Stochastic Higher than threshold
                        # 64 Intra day Stochastic Higher than threshold with delay
                        # 65 Inter day Stochastic Higher than threshold
                        # 66 Intra day Stochastic Lower than threshold
                        # 67 Intra day Stochastic Lower than threshold with delay
                        # 68 Inter day Stochastic Lower than threshold
                        # 69 Intra day Stochastic fast Higher than threshold
                        # 70 Intra day Stochastic fast Higher than threshold with delay
                        # 71 Inter day Stochastic fast Higher than threshold
                        # 72 Intra day Stochastic fast Lower than threshold
                        # 73 Intra day Stochastic fast Lower than threshold with delay
                        # 74 Inter day Stochastic fast Lower than threshold
                        # 75 Intra day Stochastic RSI Higher than threshold
                        # 76 Intra day Stochastic RSI Higher than threshold with delay
                        # 77 Inter day Stochastic RSI Higher than threshold
                        # 78 Intra day Stochastic RSI Lower than threshold
                        # 79 Intra day Stochastic RSI Lower than threshold with delay
                        # 80 Inter day Stochastic RSI Lower than threshold
                        # 81 Intra day Higher KAMA
                        # 82 Intra day Higher KAMA with delay
                        # 83 Intra day Higher KAMA with delay and maintain
                        # 84 Inter day Higher KAMA
                        # 85 Intra day in BBANDS Zone
                        # 86 Intra day Higher BBANDS with delay
                        # 87 Inter day in BBANDS Zone
                        # 88 Inter day BBANDS width change
                                    ]
    '''
    NUM_SIGNAL = len(SELECTED_SIGNAL)
    OPTIMIZATION_PARAMETER = {
        "stopLoss": {"name": "stopLoss", "value": 80, "min": 60, "max": 120, "step": 10 },
        "dollarTrailing": {"name": "dollarTrailing", "value": 150, "min": 80, "max": 200, "step": 10},
        "signalId_1": {"name": "signalId_1", "value": 1, "min": 1, "max": NUM_SIGNAL, "step": 1},
        "signalId_2": {"name": "signalId_2", "value": -1, "min": 1, "max": NUM_SIGNAL, "step": 1},
        "signalId_3": {"name": "signalId_3", "value": -1, "min": 1, "max": NUM_SIGNAL, "step": 1},
        "signalId_4": {"name": "signalId_4", "value": -1, "min": 1, "max": NUM_SIGNAL, "step": 1},
    }

    STRATEGY_NAME = "Long Signal Tester APM 5T Ordered"
    STRATEGY_SLUG = "LongSignalTesterOrderedAPM5T"
    VERSION = "1"
    LAST_UPDATE_DATE = "20190628"
    LAST_UPDATE_TIME = "150000"

    def __init__(self):
        pass

    def Setup(self, session):
        super().Setup(session)
        self.action = OrderAction.BUY
        self.tradeLimit = 1
        self.entryHourLimitInAdjustedTime = {"START": 100000, "END": 160000}
        self.minsToExitBeforeMarketClose = 30

        self.dollarTrailing = self.parameter["dollarTrailing"]["value"]

        signalNo1 = self.parameter["signalId_1"]["value"]
        signalNo2 = self.parameter["signalId_2"]["value"]
        signalNo3 = self.parameter["signalId_3"]["value"]
        signalNo4 = self.parameter["signalId_4"]["value"]

        self.SetupSignal(signalNo1)
        if signalNo2 != -1:
            self.SetupSignal(signalNo2)
            if signalNo3 != -1:
                self.SetupSignal(signalNo3)
                if signalNo4 != -1:
                    self.SetupSignal(signalNo4)

        # Exit signal
        self.stopLossSignal = exit.StopLossWithFixedPrice(self, self.stopLoss)
        #self.breakevenAfterTouchThreshold = exit.BreakevenAfterTouchThreshold(self, self.stopLoss * 2)
        self.dollarTrailingSignal = exit.DollarTrailingStop(self, self.dollarTrailing)
        #self.ExitIfNoProfitAfter = exit.ExitIfNoProfitAfter(self, 7200, 30)
        #self.fixedStopGain = exit.FixedStopGain(self, self.stopLoss*1.2)


    def CalculateEntrySignal(self, bar):
        #If All signal all pass in order
        if self.nextEntrySignalId == len(self.entrySignals):
            label = ""
            for signal in self.entrySignals:
                if label != "":
                    label += " "
                label += signal.Label()
            self.Entry(bar.closePrice, bar.adjustedDate, bar.adjustedTime, OrderType.LIMIT, label, self.baseQuantity)
            return

        nextEntrySignalId = self.nextEntrySignalId
        signal = self.entrySignals[nextEntrySignalId]

        if signal.CalculateSignal(bar):
            self.nextEntrySignalId += 1

            if self.session.mode == SessionMode.IB_LIVE or self.session.mode == SessionMode.IB_DALIY_BACKTEST:
                self.Log("Entry signal[" + str(self.session.config.sid) + "-" + signal.Label() + "]: True")
            self.CalculateBar(bar)

    def SetupSignal(self, signalId):
        # <editor-fold desc="# 1 Breakout previous day high">
        # </editor-fold>
        if signalId == 1:
            signal = entry.XHigherY(self, "close", 0, "highD", 1)
        elif signalId == 2:
            signal = entry.XHigherY(self, "close", 0, "highD", 2)
        elif signalId == 3:
            signal = entry.XHigherY(self, "close", 0, "highD", 3)
        elif signalId == 4:
            signal = entry.XHigherY(self, "close", 0, "highD", 4)
        elif signalId == 5:
            signal = entry.XHigherY(self, "close", 0, "highD", 5)
        elif signalId == 6:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "highD", 2)
        elif signalId == 7:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "highD", 3)
        elif signalId == 8:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "highD", 4)
        elif signalId == 9:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "highD", 5)
        # </editor-fold>

        # <editor-fold desc="# 2 Breakout previous day high with delay">
        elif signalId == 10:
            signal = entry.XHigherY(self, "close", 3, "highD", 1)
        elif signalId == 11:
            signal = entry.XHigherY(self, "close", 6, "highD", 1)
        elif signalId == 12:
            signal = entry.XHigherY(self, "close", 12, "highD", 1)

        elif signalId == 13:
            signal = entry.XHigherY(self, "close", 3, "highD", 2)
        elif signalId == 14:
            signal = entry.XHigherY(self, "close", 6, "highD", 2)
        elif signalId == 15:
            signal = entry.XHigherY(self, "close", 12, "highD", 2)

        elif signalId == 16:
            signal = entry.XHigherY(self, "close", 3, "highD", 3)
        elif signalId == 17:
            signal = entry.XHigherY(self, "close", 6, "highD", 3)
        elif signalId == 18:
            signal = entry.XHigherY(self, "close", 12, "highD", 3)

        elif signalId == 19:
            signal = entry.XHigherY(self, "close", 3, "highD", 4)
        elif signalId == 20:
            signal = entry.XHigherY(self, "close", 6, "highD", 4)
        elif signalId == 21:
            signal = entry.XHigherY(self, "close", 12, "highD", 4)

        elif signalId == 22:
            signal = entry.XHigherY(self, "close", 3, "highD", 5)
        elif signalId == 23:
            signal = entry.XHigherY(self, "close", 6, "highD", 5)
        elif signalId == 24:
            signal = entry.XHigherY(self, "close", 12, "highD", 5)

        elif signalId == 25:
            signal = entry.XHigherMaxPreviousY(self, "close", 3, "highD", 2)
        elif signalId == 26:
            signal = entry.XHigherMaxPreviousY(self, "close", 6, "highD", 2)
        elif signalId == 27:
            signal = entry.XHigherMaxPreviousY(self, "close", 12, "highD", 2)

        elif signalId == 28:
            signal = entry.XHigherMaxPreviousY(self, "close", 3, "highD", 3)
        elif signalId == 29:
            signal = entry.XHigherMaxPreviousY(self, "close", 6, "highD", 3)
        elif signalId == 30:
            signal = entry.XHigherMaxPreviousY(self, "close", 12, "highD", 3)

        elif signalId == 31:
            signal = entry.XHigherMaxPreviousY(self, "close", 3, "highD", 4)
        elif signalId == 32:
            signal = entry.XHigherMaxPreviousY(self, "close", 6, "highD", 4)
        elif signalId == 33:
            signal = entry.XHigherMaxPreviousY(self, "close", 12, "highD", 4)

        elif signalId == 34:
            signal = entry.XHigherMaxPreviousY(self, "close", 3, "highD", 5)
        elif signalId == 35:
            signal = entry.XHigherMaxPreviousY(self, "close", 6, "highD", 5)
        elif signalId == 36:
            signal = entry.XHigherMaxPreviousY(self, "close", 12, "highD", 5)
        # </editor-fold>

        # <editor-fold desc="# 3 Breakout previous day high with delay and maintain breakout">
        elif signalId == 37:
            signal = entry.XHigherY(self, "close", 0, "highD", 1)
            signal = entry.XHigherY(self, "close", 3, "highD", 1)
        elif signalId == 38:
            signal = entry.XHigherY(self, "close", 0, "highD", 1)
            signal = entry.XHigherY(self, "close", 6, "highD", 1)
        elif signalId == 39:
            signal = entry.XHigherY(self, "close", 0, "highD", 1)
            signal = entry.XHigherY(self, "close", 12, "highD", 1)

        elif signalId == 40:
            signal = entry.XHigherY(self, "close", 0, "highD", 2)
            signal = entry.XHigherY(self, "close", 3, "highD", 2)
        elif signalId == 41:
            signal = entry.XHigherY(self, "close", 0, "highD", 2)
            signal = entry.XHigherY(self, "close", 6, "highD", 2)
        elif signalId == 42:
            signal = entry.XHigherY(self, "close", 0, "highD", 2)
            signal = entry.XHigherY(self, "close", 12, "highD", 2)

        elif signalId == 43:
            signal = entry.XHigherY(self, "close", 0, "highD", 3)
            signal = entry.XHigherY(self, "close", 3, "highD", 3)
        elif signalId == 44:
            signal = entry.XHigherY(self, "close", 0, "highD", 3)
            signal = entry.XHigherY(self, "close", 6, "highD", 3)
        elif signalId == 45:
            signal = entry.XHigherY(self, "close", 0, "highD", 3)
            signal = entry.XHigherY(self, "close", 12, "highD", 3)

        elif signalId == 46:
            signal = entry.XHigherY(self, "close", 0, "highD", 4)
            signal = entry.XHigherY(self, "close", 3, "highD", 4)
        elif signalId == 47:
            signal = entry.XHigherY(self, "close", 0, "highD", 4)
            signal = entry.XHigherY(self, "close", 6, "highD", 4)
        elif signalId == 48:
            signal = entry.XHigherY(self, "close", 0, "highD", 4)
            signal = entry.XHigherY(self, "close", 12, "highD", 4)

        elif signalId == 49:
            signal = entry.XHigherY(self, "close", 0, "highD", 5)
            signal = entry.XHigherY(self, "close", 3, "highD", 5)
        elif signalId == 50:
            signal = entry.XHigherY(self, "close", 0, "highD", 5)
            signal = entry.XHigherY(self, "close", 6, "highD", 5)
        elif signalId == 51:
            signal = entry.XHigherY(self, "close", 0, "highD", 5)
            signal = entry.XHigherY(self, "close", 12, "highD", 5)

        elif signalId == 52:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "highD", 2)
            signal = entry.XHigherMaxPreviousY(self, "close", 3, "highD", 2)
        elif signalId == 53:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "highD", 2)
            signal = entry.XHigherMaxPreviousY(self, "close", 6, "highD", 2)
        elif signalId == 54:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "highD", 2)
            signal = entry.XHigherMaxPreviousY(self, "close", 12, "highD", 2)

        elif signalId == 55:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "highD", 3)
            signal = entry.XHigherMaxPreviousY(self, "close", 3, "highD", 3)
        elif signalId == 56:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "highD", 3)
            signal = entry.XHigherMaxPreviousY(self, "close", 6, "highD", 3)
        elif signalId == 57:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "highD", 3)
            signal = entry.XHigherMaxPreviousY(self, "close", 12, "highD", 3)

        elif signalId == 58:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "highD", 4)
            signal = entry.XHigherMaxPreviousY(self, "close", 3, "highD", 4)
        elif signalId == 59:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "highD", 4)
            signal = entry.XHigherMaxPreviousY(self, "close", 6, "highD", 4)
        elif signalId == 60:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "highD", 4)
            signal = entry.XHigherMaxPreviousY(self, "close", 12, "highD", 4)

        elif signalId == 61:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "highD", 5)
            signal = entry.XHigherMaxPreviousY(self, "close", 3, "highD", 5)
        elif signalId == 62:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "highD", 5)
            signal = entry.XHigherMaxPreviousY(self, "close", 6, "highD", 5)
        elif signalId == 63:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "highD", 5)
            signal = entry.XHigherMaxPreviousY(self, "close", 12, "highD", 5)
        # </editor-fold>

        # <editor-fold desc="# 4 Breakout previous high">
        elif signalId == 64:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 3)
        elif signalId == 65:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 6)
        elif signalId == 66:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 12)
        elif signalId == 67:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 24)
        elif signalId == 68:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 48)
        elif signalId == 69:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 60)
        # </editor-fold>

        # <editor-fold desc="# 5 Breakout previous high with delay">
        elif signalId == 70:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 3, 3, 3)
        elif signalId == 71:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 3, 6, 6)
        elif signalId == 72:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 3, 12, 12)


        elif signalId == 73:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 6, 3, 3)
        elif signalId == 74:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 6, 6, 6)
        elif signalId == 75:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 6, 12, 12)


        elif signalId == 76:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 12, 3, 3)
        elif signalId == 77:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 12, 6, 6)
        elif signalId == 78:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 12, 12, 12)


        elif signalId == 79:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 24, 3, 3)
        elif signalId == 80:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 24, 6, 6)
        elif signalId == 81:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 24, 12, 12)


        elif signalId == 82:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 48, 3, 3)
        elif signalId == 83:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 48, 6, 6)
        elif signalId == 84:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 48, 12, 12)

        elif signalId == 85:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 60, 3, 3)
        elif signalId == 86:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 60, 6, 6)
        elif signalId == 87:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 60, 12, 12)
        # </editor-fold>

        # <editor-fold desc="# 6 Breakout previous high with delay and maintain breakout">
        elif signalId == 88:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 3)
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 3, 3, 3)
        elif signalId == 89:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 3)
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 3, 6, 6)
        elif signalId == 90:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 3)
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 3, 12, 12)


        elif signalId == 91:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 6)
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 6, 3, 3)
        elif signalId == 92:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 6)
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 6, 6, 6)
        elif signalId == 93:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 6)
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 6, 12, 12)


        elif signalId == 94:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 12)
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 12, 3, 3)
        elif signalId == 95:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 12)
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 12, 6, 6)
        elif signalId == 96:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 12)
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 12, 12, 12)


        elif signalId == 97:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 24)
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 24, 3, 3)
        elif signalId == 98:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 24)
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 24, 6, 6)
        elif signalId == 99:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 24)
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 24, 12, 12)


        elif signalId == 100:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 48)
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 48, 3, 3)
        elif signalId == 101:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 48)
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 48, 6, 6)
        elif signalId == 102:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 48)
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 48, 12, 12)

        elif signalId == 103:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 60)
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 60, 3, 3)
        elif signalId == 104:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 60)
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 60, 6, 6)
        elif signalId == 105:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 60)
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "high", 60, 12, 12)
        # </editor-fold>

        # <editor-fold desc="# 7 Breakout previous day open">
        elif signalId == 106:
            signal = entry.XHigherY(self, "close", 0, "openD", 1)
        elif signalId == 107:
            signal = entry.XHigherY(self, "close", 0, "openD", 2)
        elif signalId == 108:
            signal = entry.XHigherY(self, "close", 0, "openD", 3)
        elif signalId == 109:
            signal = entry.XHigherY(self, "close", 0, "openD", 4)
        elif signalId == 110:
            signal = entry.XHigherY(self, "close", 0, "openD", 5)
        elif signalId == 111:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "openD", 2)
        elif signalId == 112:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "openD", 3)
        elif signalId == 113:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "openD", 4)
        elif signalId == 114:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "openD", 5)
        # </editor-fold>

        # <editor-fold desc="# 8 Breakout previous day open with delay">
        elif signalId == 115:
            signal = entry.XHigherY(self, "close", 3, "openD", 1)
        elif signalId == 116:
            signal = entry.XHigherY(self, "close", 6, "openD", 1)
        elif signalId == 117:
            signal = entry.XHigherY(self, "close", 12, "openD", 1)

        elif signalId == 118:
            signal = entry.XHigherY(self, "close", 3, "openD", 2)
        elif signalId == 119:
            signal = entry.XHigherY(self, "close", 6, "openD", 2)
        elif signalId == 120:
            signal = entry.XHigherY(self, "close", 12, "openD", 2)

        elif signalId == 121:
            signal = entry.XHigherY(self, "close", 3, "openD", 3)
        elif signalId == 122:
            signal = entry.XHigherY(self, "close", 6, "openD", 3)
        elif signalId == 123:
            signal = entry.XHigherY(self, "close", 12, "openD", 3)

        elif signalId == 124:
            signal = entry.XHigherY(self, "close", 3, "openD", 4)
        elif signalId == 125:
            signal = entry.XHigherY(self, "close", 6, "openD", 4)
        elif signalId == 126:
            signal = entry.XHigherY(self, "close", 12, "openD", 4)

        elif signalId == 127:
            signal = entry.XHigherY(self, "close", 3, "openD", 5)
        elif signalId == 128:
            signal = entry.XHigherY(self, "close", 6, "openD", 5)
        elif signalId == 129:
            signal = entry.XHigherY(self, "close", 12, "openD", 5)

        elif signalId == 130:
            signal = entry.XHigherMaxPreviousY(self, "close", 3, "openD", 2)
        elif signalId == 131:
            signal = entry.XHigherMaxPreviousY(self, "close", 6, "openD", 2)
        elif signalId == 132:
            signal = entry.XHigherMaxPreviousY(self, "close", 12, "openD", 2)

        elif signalId == 133:
            signal = entry.XHigherMaxPreviousY(self, "close", 3, "openD", 3)
        elif signalId == 134:
            signal = entry.XHigherMaxPreviousY(self, "close", 6, "openD", 3)
        elif signalId == 135:
            signal = entry.XHigherMaxPreviousY(self, "close", 12, "openD", 3)

        elif signalId == 136:
            signal = entry.XHigherMaxPreviousY(self, "close", 3, "openD", 4)
        elif signalId == 137:
            signal = entry.XHigherMaxPreviousY(self, "close", 6, "openD", 4)
        elif signalId == 138:
            signal = entry.XHigherMaxPreviousY(self, "close", 12, "openD", 4)

        elif signalId == 139:
            signal = entry.XHigherMaxPreviousY(self, "close", 3, "openD", 5)
        elif signalId == 140:
            signal = entry.XHigherMaxPreviousY(self, "close", 6, "openD", 5)
        elif signalId == 141:
            signal = entry.XHigherMaxPreviousY(self, "close", 12, "openD", 5)
        # </editor-fold>

        # <editor-fold desc="# 9 Breakout previous day open with delay and maintain breakout">
        elif signalId == 142:
            signal = entry.XHigherY(self, "close", 0, "openD", 1)
            signal = entry.XHigherY(self, "close", 3, "openD", 1)
        elif signalId == 143:
            signal = entry.XHigherY(self, "close", 0, "openD", 1)
            signal = entry.XHigherY(self, "close", 6, "openD", 1)
        elif signalId == 144:
            signal = entry.XHigherY(self, "close", 0, "openD", 1)
            signal = entry.XHigherY(self, "close", 12, "openD", 1)

        elif signalId == 145:
            signal = entry.XHigherY(self, "close", 0, "openD", 2)
            signal = entry.XHigherY(self, "close", 3, "openD", 2)
        elif signalId == 146:
            signal = entry.XHigherY(self, "close", 0, "openD", 2)
            signal = entry.XHigherY(self, "close", 6, "openD", 2)
        elif signalId == 147:
            signal = entry.XHigherY(self, "close", 0, "openD", 2)
            signal = entry.XHigherY(self, "close", 12, "openD", 2)

        elif signalId == 148:
            signal = entry.XHigherY(self, "close", 0, "openD", 3)
            signal = entry.XHigherY(self, "close", 3, "openD", 3)
        elif signalId == 149:
            signal = entry.XHigherY(self, "close", 0, "openD", 3)
            signal = entry.XHigherY(self, "close", 6, "openD", 3)
        elif signalId == 150:
            signal = entry.XHigherY(self, "close", 0, "openD", 3)
            signal = entry.XHigherY(self, "close", 12, "openD", 3)

        elif signalId == 151:
            signal = entry.XHigherY(self, "close", 0, "openD", 4)
            signal = entry.XHigherY(self, "close", 3, "openD", 4)
        elif signalId == 152:
            signal = entry.XHigherY(self, "close", 0, "openD", 4)
            signal = entry.XHigherY(self, "close", 6, "openD", 4)
        elif signalId == 153:
            signal = entry.XHigherY(self, "close", 0, "openD", 4)
            signal = entry.XHigherY(self, "close", 12, "openD", 4)

        elif signalId == 154:
            signal = entry.XHigherY(self, "close", 0, "openD", 5)
            signal = entry.XHigherY(self, "close", 3, "openD", 5)
        elif signalId == 155:
            signal = entry.XHigherY(self, "close", 0, "openD", 5)
            signal = entry.XHigherY(self, "close", 6, "openD", 5)
        elif signalId == 156:
            signal = entry.XHigherY(self, "close", 0, "openD", 5)
            signal = entry.XHigherY(self, "close", 12, "openD", 5)

        elif signalId == 157:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "openD", 2)
            signal = entry.XHigherMaxPreviousY(self, "close", 3, "openD", 2)
        elif signalId == 158:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "openD", 2)
            signal = entry.XHigherMaxPreviousY(self, "close", 6, "openD", 2)
        elif signalId == 159:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "openD", 2)
            signal = entry.XHigherMaxPreviousY(self, "close", 12, "openD", 2)

        elif signalId == 160:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "openD", 3)
            signal = entry.XHigherMaxPreviousY(self, "close", 3, "openD", 3)
        elif signalId == 161:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "openD", 3)
            signal = entry.XHigherMaxPreviousY(self, "close", 6, "openD", 3)
        elif signalId == 162:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "openD", 3)
            signal = entry.XHigherMaxPreviousY(self, "close", 12, "openD", 3)

        elif signalId == 163:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "openD", 4)
            signal = entry.XHigherMaxPreviousY(self, "close", 3, "openD", 4)
        elif signalId == 164:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "openD", 4)
            signal = entry.XHigherMaxPreviousY(self, "close", 6, "openD", 4)
        elif signalId == 165:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "openD", 4)
            signal = entry.XHigherMaxPreviousY(self, "close", 12, "openD", 4)

        elif signalId == 166:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "openD", 5)
            signal = entry.XHigherMaxPreviousY(self, "close", 3, "openD", 5)
        elif signalId == 167:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "openD", 5)
            signal = entry.XHigherMaxPreviousY(self, "close", 6, "openD", 5)
        elif signalId == 168:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "openD", 5)
            signal = entry.XHigherMaxPreviousY(self, "close", 12, "openD", 5)
        # </editor-fold>

        # <editor-fold desc="# 10 Breakout previous day close">
        elif signalId == 169:
            signal = entry.XHigherY(self, "close", 0, "closeD", 1)
        elif signalId == 170:
            signal = entry.XHigherY(self, "close", 0, "closeD", 2)
        elif signalId == 171:
            signal = entry.XHigherY(self, "close", 0, "closeD", 3)
        elif signalId == 172:
            signal = entry.XHigherY(self, "close", 0, "closeD", 4)
        elif signalId == 173:
            signal = entry.XHigherY(self, "close", 0, "closeD", 5)
        elif signalId == 174:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "closeD", 2)
        elif signalId == 175:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "closeD", 3)
        elif signalId == 176:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "closeD", 4)
        elif signalId == 177:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "closeD", 5)
        # </editor-fold>

        # <editor-fold desc="# 11 Breakout previous day close with delay">
        elif signalId == 178:
            signal = entry.XHigherY(self, "close", 3, "closeD", 1)
        elif signalId == 179:
            signal = entry.XHigherY(self, "close", 6, "closeD", 1)
        elif signalId == 180:
            signal = entry.XHigherY(self, "close", 12, "closeD", 1)

        elif signalId == 181:
            signal = entry.XHigherY(self, "close", 3, "closeD", 2)
        elif signalId == 182:
            signal = entry.XHigherY(self, "close", 6, "closeD", 2)
        elif signalId == 183:
            signal = entry.XHigherY(self, "close", 12, "closeD", 2)

        elif signalId == 184:
            signal = entry.XHigherY(self, "close", 3, "closeD", 3)
        elif signalId == 185:
            signal = entry.XHigherY(self, "close", 6, "closeD", 3)
        elif signalId == 186:
            signal = entry.XHigherY(self, "close", 12, "closeD", 3)

        elif signalId == 187:
            signal = entry.XHigherY(self, "close", 3, "closeD", 4)
        elif signalId == 188:
            signal = entry.XHigherY(self, "close", 6, "closeD", 4)
        elif signalId == 189:
            signal = entry.XHigherY(self, "close", 12, "closeD", 4)

        elif signalId == 190:
            signal = entry.XHigherY(self, "close", 3, "closeD", 5)
        elif signalId == 191:
            signal = entry.XHigherY(self, "close", 6, "closeD", 5)
        elif signalId == 192:
            signal = entry.XHigherY(self, "close", 12, "closeD", 5)

        elif signalId == 193:
            signal = entry.XHigherMaxPreviousY(self, "close", 3, "closeD", 2)
        elif signalId == 194:
            signal = entry.XHigherMaxPreviousY(self, "close", 6, "closeD", 2)
        elif signalId == 195:
            signal = entry.XHigherMaxPreviousY(self, "close", 12, "closeD", 2)

        elif signalId == 196:
            signal = entry.XHigherMaxPreviousY(self, "close", 3, "closeD", 3)
        elif signalId == 197:
            signal = entry.XHigherMaxPreviousY(self, "close", 6, "openD", 3)
        elif signalId == 198:
            signal = entry.XHigherMaxPreviousY(self, "close", 12, "openD", 3)

        elif signalId == 199:
            signal = entry.XHigherMaxPreviousY(self, "close", 3, "openD", 4)
        elif signalId == 200:
            signal = entry.XHigherMaxPreviousY(self, "close", 6, "openD", 4)
        elif signalId == 201:
            signal = entry.XHigherMaxPreviousY(self, "close", 12, "openD", 4)

        elif signalId == 202:
            signal = entry.XHigherMaxPreviousY(self, "close", 3, "openD", 5)
        elif signalId == 203:
            signal = entry.XHigherMaxPreviousY(self, "close", 6, "openD", 5)
        elif signalId == 204:
            signal = entry.XHigherMaxPreviousY(self, "close", 12, "openD", 5)
        # </editor-fold>

        # <editor-fold desc="# 12 Breakout previous day close with delay and maintain breakout">
        elif signalId == 205:
            signal = entry.XHigherY(self, "close", 0, "closeD", 1)
            signal = entry.XHigherY(self, "close", 3, "closeD", 1)
        elif signalId == 206:
            signal = entry.XHigherY(self, "close", 0, "closeD", 1)
            signal = entry.XHigherY(self, "close", 6, "closeD", 1)
        elif signalId == 207:
            signal = entry.XHigherY(self, "close", 0, "closeD", 1)
            signal = entry.XHigherY(self, "close", 12, "closeD", 1)

        elif signalId == 208:
            signal = entry.XHigherY(self, "close", 0, "closeD", 2)
            signal = entry.XHigherY(self, "close", 3, "closeD", 2)
        elif signalId == 209:
            signal = entry.XHigherY(self, "close", 0, "closeD", 2)
            signal = entry.XHigherY(self, "close", 6, "closeD", 2)
        elif signalId == 210:
            signal = entry.XHigherY(self, "close", 0, "closeD", 2)
            signal = entry.XHigherY(self, "close", 12, "closeD", 2)

        elif signalId == 211:
            signal = entry.XHigherY(self, "close", 0, "closeD", 3)
            signal = entry.XHigherY(self, "close", 3, "closeD", 3)
        elif signalId == 212:
            signal = entry.XHigherY(self, "close", 0, "closeD", 3)
            signal = entry.XHigherY(self, "close", 6, "closeD", 3)
        elif signalId == 213:
            signal = entry.XHigherY(self, "close", 0, "closeD", 3)
            signal = entry.XHigherY(self, "close", 12, "closeD", 3)

        elif signalId == 214:
            signal = entry.XHigherY(self, "close", 0, "closeD", 4)
            signal = entry.XHigherY(self, "close", 3, "closeD", 4)
        elif signalId == 215:
            signal = entry.XHigherY(self, "close", 0, "closeD", 4)
            signal = entry.XHigherY(self, "close", 6, "closeD", 4)
        elif signalId == 216:
            signal = entry.XHigherY(self, "close", 0, "closeD", 4)
            signal = entry.XHigherY(self, "close", 12, "closeD", 4)

        elif signalId == 217:
            signal = entry.XHigherY(self, "close", 0, "closeD", 5)
            signal = entry.XHigherY(self, "close", 3, "closeD", 5)
        elif signalId == 218:
            signal = entry.XHigherY(self, "close", 0, "closeD", 5)
            signal = entry.XHigherY(self, "close", 6, "closeD", 5)
        elif signalId == 219:
            signal = entry.XHigherY(self, "close", 0, "closeD", 5)
            signal = entry.XHigherY(self, "close", 12, "closeD", 5)

        elif signalId == 220:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "closeD", 2)
            signal = entry.XHigherMaxPreviousY(self, "close", 3, "closeD", 2)
        elif signalId == 221:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "closeD", 2)
            signal = entry.XHigherMaxPreviousY(self, "close", 6, "closeD", 2)
        elif signalId == 222:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "closeD", 2)
            signal = entry.XHigherMaxPreviousY(self, "close", 12, "closeD", 2)

        elif signalId == 223:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "closeD", 3)
            signal = entry.XHigherMaxPreviousY(self, "close", 3, "closeD", 3)
        elif signalId == 224:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "closeD", 3)
            signal = entry.XHigherMaxPreviousY(self, "close", 6, "closeD", 3)
        elif signalId == 225:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "closeD", 3)
            signal = entry.XHigherMaxPreviousY(self, "close", 12, "closeD", 3)

        elif signalId == 226:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "closeD", 4)
            signal = entry.XHigherMaxPreviousY(self, "close", 3, "closeD", 4)
        elif signalId == 227:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "closeD", 4)
            signal = entry.XHigherMaxPreviousY(self, "close", 6, "closeD", 4)
        elif signalId == 228:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "closeD", 4)
            signal = entry.XHigherMaxPreviousY(self, "close", 12, "closeD", 4)

        elif signalId == 229:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "closeD", 5)
            signal = entry.XHigherMaxPreviousY(self, "close", 3, "closeD", 5)
        elif signalId == 230:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "closeD", 5)
            signal = entry.XHigherMaxPreviousY(self, "close", 6, "closeD", 5)
        elif signalId == 231:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "closeD", 5)
            signal = entry.XHigherMaxPreviousY(self, "close", 12, "closeD", 5)
        # </editor-fold>

        # <editor-fold desc="# 13 Breakout previous low">
        elif signalId == 232:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "low", 3)
        elif signalId == 233:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "low", 6)
        elif signalId == 234:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "low", 12)
        elif signalId == 235:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "low", 24)
        elif signalId == 236:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "low", 48)
        elif signalId == 237:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "low", 60)
        # </editor-fold>

        # <editor-fold desc="# 14 Breakout previous low with delay">
        elif signalId == 238:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "low", 3, 3, 3)
        elif signalId == 239:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "low", 3, 6, 6)
        elif signalId == 240:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "low", 3, 12, 12)


        elif signalId == 241:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "low", 6, 3, 3)
        elif signalId == 242:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "low", 6, 6, 6)
        elif signalId == 243:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "low", 6, 12, 12)


        elif signalId == 244:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "low", 12, 3, 3)
        elif signalId == 245:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "low", 12, 6, 6)
        elif signalId == 246:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "low", 12, 12, 12)


        elif signalId == 247:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "low", 24, 3, 3)
        elif signalId == 248:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "low", 24, 6, 6)
        elif signalId == 249:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "low", 24, 12, 12)


        elif signalId == 250:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "low", 48, 3, 3)
        elif signalId == 251:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "low", 48, 6, 6)
        elif signalId == 252:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "low", 48, 12, 12)

        elif signalId == 253:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "low", 60, 3, 3)
        elif signalId == 254:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "low", 60, 6, 6)
        elif signalId == 255:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "low", 60, 12, 12)
        # </editor-fold>

        # <editor-fold desc="# 15 Breakout previous low with delay and maintain breakout">
        elif signalId == 256:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "low", 3)
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "low", 3, 3, 3)
        elif signalId == 257:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "low", 3)
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "low", 3, 6, 6)
        elif signalId == 258:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "low", 3)
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "low", 3, 12, 12)


        elif signalId == 259:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "low", 6)
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "low", 6, 3, 3)
        elif signalId == 260:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "low", 6)
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "low", 6, 6, 6)
        elif signalId == 261:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "low", 6)
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "low", 6, 12, 12)


        elif signalId == 262:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "low", 12)
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "low", 12, 3, 3)
        elif signalId == 263:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "low", 12)
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "low", 12, 6, 6)
        elif signalId == 264:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "low", 12)
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "low", 12, 12, 12)


        elif signalId == 265:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "low", 24)
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "low", 24, 3, 3)
        elif signalId == 266:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "low", 24)
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "low", 24, 6, 6)
        elif signalId == 267:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "low", 24)
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "low", 24, 12, 12)


        elif signalId == 268:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "low", 48)
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "low", 48, 3, 3)
        elif signalId == 269:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "low", 48)
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "low", 48, 6, 6)
        elif signalId == 270:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "low", 48)
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "low", 48, 12, 12)

        elif signalId == 271:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "low", 60)
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "low", 60, 3, 3)
        elif signalId == 272:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "low", 60)
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "low", 60, 6, 6)
        elif signalId == 273:
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "low", 60)
            signal = entry.XHigherMaxPreviousY(self, "close", 0, "low", 60, 12, 12)
        # </editor-fold>

        # <editor-fold desc="# 16 Daily higher high">
        elif signalId == 274:
            signal = entry.HigherX(self, "highD", 3)
        elif signalId == 275:
            signal = entry.HigherX(self, "highD", 5)
        elif signalId == 276:
            signal = entry.HigherX(self, "highD", 10)
        # </editor-fold>

        # <editor-fold desc="# 17 Previous day daily higher high">
        elif signalId == 277:
            signal = entry.HigherX(self, "highD", 3, 1)
        elif signalId == 278:
            signal = entry.HigherX(self, "highD", 5, 1)
        elif signalId == 279:
            signal = entry.HigherX(self, "highD", 10, 1)
        elif signalId == 280:
            signal = entry.HigherX(self, "highD", 3, 2)
        elif signalId == 281:
            signal = entry.HigherX(self, "highD", 5, 2)
        elif signalId == 282:
            signal = entry.HigherX(self, "highD", 10, 2)
        elif signalId == 283:
            signal = entry.HigherX(self, "highD", 3, 3)
        elif signalId == 284:
            signal = entry.HigherX(self, "highD", 5, 3)
        elif signalId == 285:
            signal = entry.HigherX(self, "highD", 10, 3)
        elif signalId == 286:
            signal = entry.HigherX(self, "highD", 3, 5)
        elif signalId == 287:
            signal = entry.HigherX(self, "highD", 5, 5)
        elif signalId == 288:
            signal = entry.HigherX(self, "highD", 10, 5)
        # </editor-fold>

        # <editor-fold desc="# 18 Daily higher low">
        elif signalId == 289:
            signal = entry.HigherX(self, "lowD", 3)
        elif signalId == 290:
            signal = entry.HigherX(self, "lowD", 5)
        elif signalId == 291:
            signal = entry.HigherX(self, "lowD", 10)
        # </editor-fold>

        # <editor-fold desc="# 19 Previous day daily higher low">
        elif signalId == 292:
            signal = entry.HigherX(self, "lowD", 3, 1)
        elif signalId == 293:
            signal = entry.HigherX(self, "lowD", 5, 1)
        elif signalId == 294:
            signal = entry.HigherX(self, "lowD", 10, 1)
        elif signalId == 295:
            signal = entry.HigherX(self, "lowD", 3, 2)
        elif signalId == 296:
            signal = entry.HigherX(self, "lowD", 5, 2)
        elif signalId == 297:
            signal = entry.HigherX(self, "lowD", 10, 2)
        elif signalId == 298:
            signal = entry.HigherX(self, "lowD", 3, 3)
        elif signalId == 299:
            signal = entry.HigherX(self, "lowD", 5, 3)
        elif signalId == 300:
            signal = entry.HigherX(self, "lowD", 10, 3)
        elif signalId == 301:
            signal = entry.HigherX(self, "lowD", 3, 5)
        elif signalId == 302:
            signal = entry.HigherX(self, "lowD", 5, 5)
        elif signalId == 303:
            signal = entry.HigherX(self, "lowD", 10, 5)
        # </editor-fold>

        # <editor-fold desc="# 20 Daily lower high">
        elif signalId == 304:
            signal = entry.LowerX(self, "highD", 3)
        elif signalId == 305:
            signal = entry.LowerX(self, "highD", 5)
        elif signalId == 306:
            signal = entry.LowerX(self, "highD", 10)
        # </editor-fold>

        # <editor-fold desc="# 21 Previous day daily lower high">
        elif signalId == 307:
            signal = entry.LowerX(self, "highD", 3, 1)
        elif signalId == 308:
            signal = entry.LowerX(self, "highD", 5, 1)
        elif signalId == 309:
            signal = entry.LowerX(self, "highD", 10, 1)
        elif signalId == 310:
            signal = entry.LowerX(self, "highD", 3, 2)
        elif signalId == 311:
            signal = entry.LowerX(self, "highD", 5, 2)
        elif signalId == 312:
            signal = entry.LowerX(self, "highD", 10, 2)
        elif signalId == 313:
            signal = entry.LowerX(self, "highD", 3, 3)
        elif signalId == 314:
            signal = entry.LowerX(self, "highD", 5, 3)
        elif signalId == 315:
            signal = entry.LowerX(self, "highD", 10, 3)
        elif signalId == 316:
            signal = entry.LowerX(self, "highD", 3, 5)
        elif signalId == 317:
            signal = entry.LowerX(self, "highD", 5, 5)
        elif signalId == 318:
            signal = entry.LowerX(self, "highD", 10, 5)
        # </editor-fold>

        # <editor-fold desc="# 22 Daily lower low">
        elif signalId == 319:
            signal = entry.LowerX(self, "lowD", 3)
        elif signalId == 320:
            signal = entry.LowerX(self, "lowD", 5)
        elif signalId == 321:
            signal = entry.LowerX(self, "lowD", 10)
        # </editor-fold>

        # <editor-fold desc="# 23 Previous day daily lower low">
        elif signalId == 322:
            signal = entry.LowerX(self, "lowD", 3, 1)
        elif signalId == 323:
            signal = entry.LowerX(self, "lowD", 5, 1)
        elif signalId == 324:
            signal = entry.LowerX(self, "lowD", 10, 1)
        elif signalId == 325:
            signal = entry.LowerX(self, "lowD", 3, 2)
        elif signalId == 326:
            signal = entry.LowerX(self, "lowD", 5, 2)
        elif signalId == 327:
            signal = entry.LowerX(self, "lowD", 10, 2)
        elif signalId == 328:
            signal = entry.LowerX(self, "lowD", 3, 3)
        elif signalId == 329:
            signal = entry.LowerX(self, "lowD", 5, 3)
        elif signalId == 330:
            signal = entry.LowerX(self, "lowD", 10, 3)
        elif signalId == 331:
            signal = entry.LowerX(self, "lowD", 3, 5)
        elif signalId == 332:
            signal = entry.LowerX(self, "lowD", 5, 5)
        elif signalId == 333:
            signal = entry.LowerX(self, "lowD", 10, 5)
        # </editor-fold>

        # <editor-fold desc="# 24 Intra day higher high">
        elif signalId == 334:
            signal = entry.HigherX(self, "high", 3)
        elif signalId == 335:
            signal = entry.HigherX(self, "high", 6)
        elif signalId == 336:
            signal = entry.HigherX(self, "high", 9)
        elif signalId == 337:
            signal = entry.HigherX(self, "high", 12)
        # </editor-fold>

        # <editor-fold desc="# 25 Intra day higher high with delay">
        elif signalId == 338:
            signal = entry.HigherX(self, "high", 3, 3)
        elif signalId == 339:
            signal = entry.HigherX(self, "high", 6, 3)
        elif signalId == 340:
            signal = entry.HigherX(self, "high", 9, 3)
        elif signalId == 341:
            signal = entry.HigherX(self, "high", 12, 6)
        elif signalId == 342:
            signal = entry.HigherX(self, "high", 3, 6)
        elif signalId == 343:
            signal = entry.HigherX(self, "high", 6, 6)
        elif signalId == 344:
            signal = entry.HigherX(self, "high", 9, 6)
        elif signalId == 345:
            signal = entry.HigherX(self, "high", 12, 6)
        elif signalId == 346:
            signal = entry.HigherX(self, "high", 3, 9)
        elif signalId == 347:
            signal = entry.HigherX(self, "high", 6, 9)
        elif signalId == 348:
            signal = entry.HigherX(self, "high", 9, 9)
        elif signalId == 349:
            signal = entry.HigherX(self, "high", 12, 9)
        elif signalId == 350:
            signal = entry.HigherX(self, "high", 3, 12)
        elif signalId == 351:
            signal = entry.HigherX(self, "high", 6, 12)
        elif signalId == 352:
            signal = entry.HigherX(self, "high", 9, 12)
        elif signalId == 353:
            signal = entry.HigherX(self, "high", 12, 12)
        # </editor-fold>

        # <editor-fold desc="# 26 Intra day higher low">
        elif signalId == 354:
            signal = entry.HigherX(self, "low", 3)
        elif signalId == 355:
            signal = entry.HigherX(self, "low", 6)
        elif signalId == 356:
            signal = entry.HigherX(self, "low", 9)
        elif signalId == 357:
            signal = entry.HigherX(self, "low", 12)
        # </editor-fold>

        # <editor-fold desc="# 27 Intra day higher low with delay">
        elif signalId == 358:
            signal = entry.HigherX(self, "low", 3, 3)
        elif signalId == 359:
            signal = entry.HigherX(self, "low", 6, 3)
        elif signalId == 360:
            signal = entry.HigherX(self, "low", 9, 3)
        elif signalId == 361:
            signal = entry.HigherX(self, "low", 12, 6)
        elif signalId == 362:
            signal = entry.HigherX(self, "low", 3, 6)
        elif signalId == 363:
            signal = entry.HigherX(self, "low", 6, 6)
        elif signalId == 364:
            signal = entry.HigherX(self, "low", 9, 6)
        elif signalId == 365:
            signal = entry.HigherX(self, "low", 12, 6)
        elif signalId == 366:
            signal = entry.HigherX(self, "low", 3, 9)
        elif signalId == 367:
            signal = entry.HigherX(self, "low", 6, 9)
        elif signalId == 368:
            signal = entry.HigherX(self, "low", 9, 9)
        elif signalId == 369:
            signal = entry.HigherX(self, "low", 12, 9)
        elif signalId == 370:
            signal = entry.HigherX(self, "low", 3, 12)
        elif signalId == 371:
            signal = entry.HigherX(self, "low", 6, 12)
        elif signalId == 372:
            signal = entry.HigherX(self, "low", 9, 12)
        elif signalId == 373:
            signal = entry.HigherX(self, "low", 12, 12)
        # </editor-fold>

        # <editor-fold desc="# 28 Intra day lower high">
        elif signalId == 374:
            signal = entry.LowerX(self, "high", 3)
        elif signalId == 375:
            signal = entry.LowerX(self, "high", 6)
        elif signalId == 376:
            signal = entry.LowerX(self, "high", 9)
        elif signalId == 377:
            signal = entry.LowerX(self, "high", 12)
        # </editor-fold>

        # <editor-fold desc="# 29 Intra day lower high with delay">
        elif signalId == 378:
            signal = entry.LowerX(self, "high", 3, 3)
        elif signalId == 379:
            signal = entry.LowerX(self, "high", 6, 3)
        elif signalId == 380:
            signal = entry.LowerX(self, "high", 9, 3)
        elif signalId == 381:
            signal = entry.LowerX(self, "high", 12, 6)
        elif signalId == 382:
            signal = entry.LowerX(self, "high", 3, 6)
        elif signalId == 383:
            signal = entry.LowerX(self, "high", 6, 6)
        elif signalId == 384:
            signal = entry.LowerX(self, "high", 9, 6)
        elif signalId == 385:
            signal = entry.LowerX(self, "high", 12, 6)
        elif signalId == 386:
            signal = entry.LowerX(self, "high", 3, 9)
        elif signalId == 387:
            signal = entry.LowerX(self, "high", 6, 9)
        elif signalId == 388:
            signal = entry.LowerX(self, "high", 9, 9)
        elif signalId == 389:
            signal = entry.LowerX(self, "high", 12, 9)
        elif signalId == 390:
            signal = entry.LowerX(self, "high", 3, 12)
        elif signalId == 391:
            signal = entry.LowerX(self, "high", 6, 12)
        elif signalId == 392:
            signal = entry.LowerX(self, "high", 9, 12)
        elif signalId == 393:
            signal = entry.LowerX(self, "high", 12, 12)
        # </editor-fold>

        # <editor-fold desc="# 30 Intra day lower low">
        elif signalId == 394:
            signal = entry.LowerX(self, "low", 3)
        elif signalId == 395:
            signal = entry.LowerX(self, "low", 6)
        elif signalId == 396:
            signal = entry.LowerX(self, "low", 9)
        elif signalId == 397:
            signal = entry.LowerX(self, "low", 12)
        # </editor-fold>

        # <editor-fold desc="# 31 Intra day lower low with delay">
        elif signalId == 398:
            signal = entry.LowerX(self, "low", 3, 3)
        elif signalId == 399:
            signal = entry.LowerX(self, "low", 6, 3)
        elif signalId == 400:
            signal = entry.LowerX(self, "low", 9, 3)
        elif signalId == 401:
            signal = entry.LowerX(self, "low", 12, 6)
        elif signalId == 402:
            signal = entry.LowerX(self, "low", 3, 6)
        elif signalId == 403:
            signal = entry.LowerX(self, "low", 6, 6)
        elif signalId == 404:
            signal = entry.LowerX(self, "low", 9, 6)
        elif signalId == 405:
            signal = entry.LowerX(self, "low", 12, 6)
        elif signalId == 406:
            signal = entry.LowerX(self, "low", 3, 9)
        elif signalId == 407:
            signal = entry.LowerX(self, "low", 6, 9)
        elif signalId == 408:
            signal = entry.LowerX(self, "low", 9, 9)
        elif signalId == 409:
            signal = entry.LowerX(self, "low", 12, 9)
        elif signalId == 410:
            signal = entry.LowerX(self, "low", 3, 12)
        elif signalId == 411:
            signal = entry.LowerX(self, "low", 6, 12)
        elif signalId == 412:
            signal = entry.LowerX(self, "low", 9, 12)
        elif signalId == 413:
            signal = entry.LowerX(self, "low", 12, 12)
        # </editor-fold>

        # <editor-fold desc="# 32 Intra day higher high and higer low">
        elif signalId == 414:
            signal = entry.HigherX(self, "high", 3)
            signal = entry.HigherX(self, "low", 3)
        elif signalId == 415:
            signal = entry.HigherX(self, "high", 6)
            signal = entry.HigherX(self, "low", 6)
        elif signalId == 416:
            signal = entry.HigherX(self, "high", 9)
            signal = entry.HigherX(self, "low", 9)
        elif signalId == 417:
            signal = entry.HigherX(self, "high", 12)
            signal = entry.HigherX(self, "low", 12)
        # </editor-fold>

        # <editor-fold desc="# 33 Intra day higher high and higer low with delay">
        elif signalId == 418:
            signal = entry.HigherX(self, "high", 3, 3)
            signal = entry.HigherX(self, "low", 3, 3)
        elif signalId == 419:
            signal = entry.HigherX(self, "high", 6, 3)
            signal = entry.HigherX(self, "low", 6, 3)
        elif signalId == 420:
            signal = entry.HigherX(self, "high", 9, 3)
            signal = entry.HigherX(self, "low", 9, 3)
        elif signalId == 421:
            signal = entry.HigherX(self, "high", 12, 6)
            signal = entry.HigherX(self, "low", 12, 6)
        elif signalId == 422:
            signal = entry.HigherX(self, "high", 3, 6)
            signal = entry.HigherX(self, "low", 3, 6)
        elif signalId == 423:
            signal = entry.HigherX(self, "high", 6, 6)
            signal = entry.HigherX(self, "low", 6, 6)
        elif signalId == 424:
            signal = entry.HigherX(self, "high", 9, 6)
            signal = entry.HigherX(self, "low", 9, 6)
        elif signalId == 425:
            signal = entry.HigherX(self, "high", 12, 6)
            signal = entry.HigherX(self, "low", 12, 6)
        elif signalId == 426:
            signal = entry.HigherX(self, "high", 3, 9)
            signal = entry.HigherX(self, "low", 3, 9)
        elif signalId == 427:
            signal = entry.HigherX(self, "high", 6, 9)
            signal = entry.HigherX(self, "low", 6, 9)
        elif signalId == 428:
            signal = entry.HigherX(self, "high", 9, 9)
            signal = entry.HigherX(self, "low", 9, 9)
        elif signalId == 429:
            signal = entry.HigherX(self, "high", 12, 9)
            signal = entry.HigherX(self, "low", 12, 9)
        elif signalId == 430:
            signal = entry.HigherX(self, "high", 3, 12)
            signal = entry.HigherX(self, "low", 3, 12)
        elif signalId == 431:
            signal = entry.HigherX(self, "high", 6, 12)
            signal = entry.HigherX(self, "low", 6, 12)
        elif signalId == 432:
            signal = entry.HigherX(self, "high", 9, 12)
            signal = entry.HigherX(self, "low", 9, 12)
        elif signalId == 433:
            signal = entry.HigherX(self, "high", 12, 12)
            signal = entry.HigherX(self, "low", 12, 12)
        # </editor-fold>

        # <editor-fold desc="# 34 Day open inside pivot point zone">
        elif signalId == 434:
            signal = entry.XHigherPivotPoint(self, "openD", 0, 1)
            signal = entry.XLowerPivotPointR1(self, "openD", 0, 1)
        elif signalId == 435:
            signal = entry.XHigherPivotPointR1(self, "openD", 0, 1)
            signal = entry.XLowerPivotPointR2(self, "openD", 0, 1)
        elif signalId == 436:
            signal = entry.XHigherPivotPointR2(self, "openD", 0, 1)
            signal = entry.XLowerPivotPointR3(self, "openD", 0, 1)
        elif signalId == 437:
            signal = entry.XLowerPivotPoint(self, "openD", 0, 1)
            signal = entry.XHigherPivotPointS1(self, "openD", 0, 1)
        elif signalId == 438:
            signal = entry.XLowerPivotPointS1(self, "openD", 0, 1)
            signal = entry.XHigherPivotPointS2(self, "openD", 0, 1)
        elif signalId == 439:
            signal = entry.XLowerPivotPointS2(self, "openD", 0, 1)
            signal = entry.XHigherPivotPointS3(self, "openD", 0, 1)
        # </editor-fold>

        # <editor-fold desc="# 35 Close inside pivot point zone">
        elif signalId == 440:
            signal = entry.XHigherPivotPoint(self, "close", 0, 1)
            signal = entry.XLowerPivotPointR1(self, "close", 0, 1)
        elif signalId == 441:
            signal = entry.XHigherPivotPointR1(self, "close", 0, 1)
            signal = entry.XLowerPivotPointR2(self, "close", 0, 1)
        elif signalId == 442:
            signal = entry.XHigherPivotPointR2(self, "close", 0, 1)
            signal = entry.XLowerPivotPointR3(self, "close", 0, 1)
        elif signalId == 443:
            signal = entry.XLowerPivotPoint(self, "close", 0, 1)
            signal = entry.XHigherPivotPointS1(self, "close", 0, 1)
        elif signalId == 444:
            signal = entry.XLowerPivotPointS1(self, "close", 0, 1)
            signal = entry.XHigherPivotPointS2(self, "close", 0, 1)
        elif signalId == 445:
            signal = entry.XLowerPivotPointS2(self, "close", 0, 1)
            signal = entry.XHigherPivotPointS3(self, "close", 0, 1)
        # </editor-fold>

        # <editor-fold desc="# 36 Min RSI Higher threshold related">
        elif signalId == 446:
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 0, 3, 80)
        elif signalId == 447:
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 0, 6, 80)
        elif signalId == 448:
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 0, 9, 80)
        elif signalId == 449:
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 0, 12, 80)
        # </editor-fold>

        # <editor-fold desc="# 37 Min RSI Higher threshold related with delay">
        elif signalId == 450:
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 3, 3, 80)
        elif signalId == 451:
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 3, 6, 80)
        elif signalId == 452:
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 3, 9, 80)
        elif signalId == 453:
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 3, 12, 80)

        elif signalId == 454:
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 6, 3, 80)
        elif signalId == 455:
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 6, 6, 80)
        elif signalId == 456:
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 6, 9, 80)
        elif signalId == 457:
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 6, 12, 80)

        elif signalId == 458:
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 9, 3, 80)
        elif signalId == 459:
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 9, 6, 80)
        elif signalId == 460:
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 9, 9, 80)
        elif signalId == 461:
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 9, 12, 80)

        elif signalId == 462:
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 12, 3, 80)
        elif signalId == 463:
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 12, 6, 80)
        elif signalId == 464:
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 12, 9, 80)
        elif signalId == 465:
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 12, 12, 80)
        # </editor-fold>

        # <editor-fold desc="# 38 Min RSI Higher threshold related with delay and maintain threshold level">
        elif signalId == 466:
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 0, 3, 80)
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 3, 3, 80)
        elif signalId == 467:
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 0, 6, 80)
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 3, 6, 80)
        elif signalId == 468:
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 0, 9, 80)
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 3, 9, 80)
        elif signalId == 469:
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 0, 12, 80)
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 3, 12, 80)

        elif signalId == 470:
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 0, 0, 80)
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 6, 3, 80)
        elif signalId == 471:
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 0, 6, 80)
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 6, 6, 80)
        elif signalId == 472:
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 0, 9, 80)
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 6, 9, 80)
        elif signalId == 473:
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 0, 12, 80)
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 6, 12, 80)

        elif signalId == 474:
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 0, 3, 80)
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 9, 3, 80)
        elif signalId == 475:
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 0, 6, 80)
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 9, 6, 80)
        elif signalId == 476:
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 0, 9, 80)
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 9, 9, 80)
        elif signalId == 477:
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 0, 12, 80)
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 9, 12, 80)
        # </editor-fold>

        # <editor-fold desc="# 39 Min RSI Higher threshold related with delay and cannot maintain threshold level">
        elif signalId == 478:
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 0, 3, 80)
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 3, 3, 80)
        elif signalId == 479:
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 0, 6, 80)
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 3, 6, 80)
        elif signalId == 480:
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 0, 9, 80)
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 3, 9, 80)
        elif signalId == 481:
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 0, 12, 80)
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 3, 12, 80)

        elif signalId == 482:
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 0, 3, 80)
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 6, 3, 80)
        elif signalId == 483:
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 0, 6, 80)
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 6, 6, 80)
        elif signalId == 484:
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 0, 9, 80)
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 6, 9, 80)
        elif signalId == 485:
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 0, 12, 80)
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 6, 12, 80)

        elif signalId == 486:
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 0, 3, 80)
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 9, 3, 80)
        elif signalId == 487:
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 0, 6, 80)
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 9, 6, 80)
        elif signalId == 488:
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 0, 9, 80)
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 9, 9, 80)
        elif signalId == 489:
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 0, 12, 80)
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 9, 12, 80)
        # </editor-fold>

        # <editor-fold desc="# 40 Max RSI Lower threshold related">
        elif signalId == 490:
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 0, 3, 20)
        elif signalId == 491:
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 0, 6, 20)
        elif signalId == 492:
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 0, 9, 20)
        elif signalId == 493:
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 0, 12, 20)
        # </editor-fold>

        # <editor-fold desc="# 41 Max RSI Lower threshold related with delay">
        elif signalId == 494:
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 3, 3, 20)
        elif signalId == 495:
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 3, 6, 20)
        elif signalId == 496:
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 3, 9, 20)
        elif signalId == 497:
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 3, 12, 20)

        elif signalId == 498:
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 6, 3, 20)
        elif signalId == 499:
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 6, 6, 20)
        elif signalId == 500:
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 6, 9, 20)
        elif signalId == 501:
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 6, 12, 20)

        elif signalId == 502:
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 9, 3, 20)
        elif signalId == 503:
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 9, 6, 20)
        elif signalId == 504:
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 9, 9, 20)
        elif signalId == 505:
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 9, 12, 20)

        elif signalId == 506:
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 12, 3, 20)
        elif signalId == 507:
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 12, 6, 20)
        elif signalId == 508:
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 12, 9, 20)
        elif signalId == 509:
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 12, 12, 20)
        # </editor-fold>

        # <editor-fold desc="# 42 Max RSI Lower threshold related with delay and maintain threshold level">
        elif signalId == 510:
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 0, 3, 20)
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 3, 3, 20)
        elif signalId == 511:
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 0, 6, 20)
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 3, 6, 20)
        elif signalId == 512:
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 0, 9, 20)
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 3, 9, 20)
        elif signalId == 513:
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 0, 12, 20)
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 3, 12, 20)

        elif signalId == 514:
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 0, 0, 20)
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 6, 3, 20)
        elif signalId == 515:
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 0, 6, 20)
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 6, 6, 20)
        elif signalId == 516:
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 0, 9, 20)
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 6, 9, 20)
        elif signalId == 517:
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 0, 12, 20)
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 6, 12, 20)

        elif signalId == 518:
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 0, 3, 20)
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 9, 3, 20)
        elif signalId == 519:
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 0, 6, 20)
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 9, 6, 20)
        elif signalId == 520:
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 0, 9, 20)
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 9, 9, 20)
        elif signalId == 521:
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 0, 12, 20)
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 9, 12, 20)
        # </editor-fold>

        # <editor-fold desc="# 43 Max RSI Lower threshold related with delay and cannot maintain threshold level">
        elif signalId == 522:
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 0, 3, 20)
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 3, 3, 20)
        elif signalId == 523:
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 0, 6, 20)
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 3, 6, 20)
        elif signalId == 524:
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 0, 9, 20)
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 3, 9, 20)
        elif signalId == 525:
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 0, 12, 20)
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 3, 12, 20)
        elif signalId == 526:
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 0, 3, 20)
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 6, 3, 20)
        elif signalId == 527:
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 0, 6, 20)
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 6, 6, 20)
        elif signalId == 528:
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 0, 9, 20)
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 6, 9, 20)
        elif signalId == 529:
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 0, 12, 20)
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 6, 12, 20)
        elif signalId == 530:
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 0, 3, 20)
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 12, 3, 20)
        elif signalId == 531:
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 0, 6, 20)
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 12, 6, 20)
        elif signalId == 532:
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 0, 9, 20)
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 12, 9, 20)
        elif signalId == 533:
            signal = entry.MinRSIHigherThreshold(self, "close", 14, 0, 12, 20)
            signal = entry.MaxRSILowerThreshold(self, "close", 14, 12, 12, 20)
        # </editor-fold>

        # <editor-fold desc="# 44 close higher SMA related">
        elif signalId == 534:
            signal = entry.XHigherAverageY(self, "close", 0, "close", 10)
        elif signalId == 535:
            signal = entry.XHigherAverageY(self, "close", 0, "close", 20)
        elif signalId == 536:
            signal = entry.XHigherAverageY(self, "close", 0, "close", 30)
        elif signalId == 537:
            signal = entry.XHigherAverageY(self, "close", 0, "close", 40)
        # </editor-fold>

        # <editor-fold desc="# 45 close higher SMA related with delay">
        elif signalId == 538:
            signal = entry.XHigherAverageY(self, "close", 0, "close", 10, 3, 3)
        elif signalId == 539:
            signal = entry.XHigherAverageY(self, "close", 0, "close", 20, 3, 3)
        elif signalId == 540:
            signal = entry.XHigherAverageY(self, "close", 0, "close", 30, 3, 3)
        elif signalId == 541:
            signal = entry.XHigherAverageY(self, "close", 0, "close", 40, 3, 3)
        elif signalId == 542:
            signal = entry.XHigherAverageY(self, "close", 0, "close", 10, 6, 6)
        elif signalId == 543:
            signal = entry.XHigherAverageY(self, "close", 0, "close", 20, 6, 6)
        elif signalId == 544:
            signal = entry.XHigherAverageY(self, "close", 0, "close", 30, 6, 6)
        elif signalId == 545:
            signal = entry.XHigherAverageY(self, "close", 0, "close", 40, 6, 6)
        elif signalId == 546:
            signal = entry.XHigherAverageY(self, "close", 0, "close", 10, 12, 12)
        elif signalId == 547:
            signal = entry.XHigherAverageY(self, "close", 0, "close", 20, 12, 12)
        elif signalId == 548:
            signal = entry.XHigherAverageY(self, "close", 0, "close", 30, 12, 12)
        elif signalId == 549:
            signal = entry.XHigherAverageY(self, "close", 0, "close", 40, 12, 12)
        # </editor-fold>

        # <editor-fold desc="# 46 close higher SMA related with delay and maintain breakout">
        elif signalId == 550:
            signal = entry.XHigherAverageY(self, "close", 0, "close", 10)
            signal = entry.XHigherAverageY(self, "close", 0, "close", 10, 3, 3)
        elif signalId == 551:
            signal = entry.XHigherAverageY(self, "close", 0, "close", 20)
            signal = entry.XHigherAverageY(self, "close", 0, "close", 20, 3, 3)
        elif signalId == 552:
            signal = entry.XHigherAverageY(self, "close", 0, "close", 30)
            signal = entry.XHigherAverageY(self, "close", 0, "close", 30, 3, 3)
        elif signalId == 553:
            signal = entry.XHigherAverageY(self, "close", 0, "close", 40)
            signal = entry.XHigherAverageY(self, "close", 0, "close", 40, 3, 3)
        elif signalId == 554:
            signal = entry.XHigherAverageY(self, "close", 0, "close", 10)
            signal = entry.XHigherAverageY(self, "close", 0, "close", 10, 6, 6)
        elif signalId == 555:
            signal = entry.XHigherAverageY(self, "close", 0, "close", 20)
            signal = entry.XHigherAverageY(self, "close", 0, "close", 20, 6, 6)
        elif signalId == 556:
            signal = entry.XHigherAverageY(self, "close", 0, "close", 30)
            signal = entry.XHigherAverageY(self, "close", 0, "close", 30, 6, 6)
        elif signalId == 557:
            signal = entry.XHigherAverageY(self, "close", 0, "close", 40)
            signal = entry.XHigherAverageY(self, "close", 0, "close", 40, 6, 6)
        elif signalId == 558:
            signal = entry.XHigherAverageY(self, "close", 0, "close", 10)
            signal = entry.XHigherAverageY(self, "close", 0, "close", 10, 12, 12)
        elif signalId == 559:
            signal = entry.XHigherAverageY(self, "close", 0, "close", 20)
            signal = entry.XHigherAverageY(self, "close", 0, "close", 20, 12, 12)
        elif signalId == 560:
            signal = entry.XHigherAverageY(self, "close", 0, "close", 30)
            signal = entry.XHigherAverageY(self, "close", 0, "close", 30, 12, 12)
        elif signalId == 561:
            signal = entry.XHigherAverageY(self, "close", 0, "close", 40)
            signal = entry.XHigherAverageY(self, "close", 0, "close", 40, 12, 12)
        # </editor-fold>

        # <editor-fold desc="# 47 close SMA cross">
        elif signalId == 562:
            signal = entry.AverageXHigherAverageY(self, "close", 3, "close", 12)
        elif signalId == 563:
            signal = entry.AverageXHigherAverageY(self, "close", 4, "close", 16)
        elif signalId == 564:
            signal = entry.AverageXHigherAverageY(self, "close", 6, "close", 24)
        elif signalId == 565:
            signal = entry.AverageXHigherAverageY(self, "close", 8, "close", 32)
        elif signalId == 566:
            signal = entry.AverageXHigherAverageY(self, "close", 10, "close", 40)
        elif signalId == 567:
            signal = entry.AverageXHigherAverageY(self, "close", 12, "close", 48)
        # </editor-fold>

        # <editor-fold desc="# 48 Close Higher Morning OHLC">
        elif signalId == 568:
            signal = entry.XHigherY(self, "close", 0, "morningOpenD", 0)
        elif signalId == 569:
            signal = entry.XHigherY(self, "close", 0, "morningHighD", 0)
        elif signalId == 570:
            signal = entry.XHigherY(self, "close", 0, "morningLowD", 0)
        elif signalId == 571:
            signal = entry.XHigherY(self, "close", 0, "morningCloseD", 0)
        # </editor-fold>

        # <editor-fold desc="# 49 Close Higher Morning OHLC with delay">
        elif signalId == 572:
            signal = entry.XHigherY(self, "close", 3, "morningOpenD", 0)
        elif signalId == 573:
            signal = entry.XHigherY(self, "close", 3, "morningHighD", 0)
        elif signalId == 574:
            signal = entry.XHigherY(self, "close", 3, "morningLowD", 0)
        elif signalId == 575:
            signal = entry.XHigherY(self, "close", 3, "morningCloseD", 0)

        elif signalId == 576:
            signal = entry.XHigherY(self, "close", 6, "morningOpenD", 0)
        elif signalId == 577:
            signal = entry.XHigherY(self, "close", 6, "morningHighD", 0)
        elif signalId == 578:
            signal = entry.XHigherY(self, "close", 6, "morningLowD", 0)
        elif signalId == 579:
            signal = entry.XHigherY(self, "close", 6, "morningCloseD", 0)

        elif signalId == 580:
            signal = entry.XHigherY(self, "close", 12, "morningOpenD", 0)
        elif signalId == 581:
            signal = entry.XHigherY(self, "close", 12, "morningHighD", 0)
        elif signalId == 582:
            signal = entry.XHigherY(self, "close", 12, "morningLowD", 0)
        elif signalId == 583:
            signal = entry.XHigherY(self, "close", 12, "morningCloseD", 0)
        # </editor-fold>

        # <editor-fold desc="# 50 Close Higher Morning OHLC with delay and maintain breakout">
        elif signalId == 584:
            signal = entry.XHigherY(self, "close", 0, "morningOpenD", 0)
            signal = entry.XHigherY(self, "close", 3, "morningOpenD", 0)
        elif signalId == 585:
            signal = entry.XHigherY(self, "close", 0, "morningHighD", 0)
            signal = entry.XHigherY(self, "close", 3, "morningHighD", 0)
        elif signalId == 586:
            signal = entry.XHigherY(self, "close", 0, "morningLowD", 0)
            signal = entry.XHigherY(self, "close", 3, "morningLowD", 0)
        elif signalId == 587:
            signal = entry.XHigherY(self, "close", 0, "morningCloseD", 0)
            signal = entry.XHigherY(self, "close", 3, "morningCloseD", 0)

        elif signalId == 588:
            signal = entry.XHigherY(self, "close", 0, "morningOpenD", 0)
            signal = entry.XHigherY(self, "close", 6, "morningOpenD", 0)
        elif signalId == 589:
            signal = entry.XHigherY(self, "close", 0, "morningHighD", 0)
            signal = entry.XHigherY(self, "close", 6, "morningHighD", 0)
        elif signalId == 590:
            signal = entry.XHigherY(self, "close", 0, "morningLowD", 0)
            signal = entry.XHigherY(self, "close", 6, "morningLowD", 0)
        elif signalId == 591:
            signal = entry.XHigherY(self, "close", 0, "morningCloseD", 0)
            signal = entry.XHigherY(self, "close", 6, "morningCloseD", 0)

        elif signalId == 592:
            signal = entry.XHigherY(self, "close", 0, "morningOpenD", 0)
            signal = entry.XHigherY(self, "close", 12, "morningOpenD", 0)
        elif signalId == 593:
            signal = entry.XHigherY(self, "close", 0, "morningHighD", 0)
            signal = entry.XHigherY(self, "close", 12, "morningHighD", 0)
        elif signalId == 594:
            signal = entry.XHigherY(self, "close", 0, "morningLowD", 0)
            signal = entry.XHigherY(self, "close", 12, "morningLowD", 0)
        elif signalId == 595:
            signal = entry.XHigherY(self, "close", 0, "morningCloseD", 0)
            signal = entry.XHigherY(self, "close", 12, "morningCloseD", 0)
        # </editor-fold>

        # <editor-fold desc="# 51 Intra day MACD cross">
        elif signalId == 596:
            signal = entry.MACDHigherMACDSignal(self, "close", 6, 13, 4)
        elif signalId == 597:
            signal = entry.MACDHigherMACDSignal(self, "close", 12, 26, 9)
        elif signalId == 598:
            signal = entry.MACDHigherMACDSignal(self, "close", 18, 39, 14)
        # </editor-fold>

        # <editor-fold desc="# 52 Intra day MACD cross with delay">
        elif signalId == 599:
            signal = entry.MACDHigherMACDSignal(self, "close", 6, 13, 4, 3)
        elif signalId == 600:
            signal = entry.MACDHigherMACDSignal(self, "close", 12, 26, 9, 3)
        elif signalId == 601:
            signal = entry.MACDHigherMACDSignal(self, "close", 18, 39, 14, 3)

        elif signalId == 602:
            signal = entry.MACDHigherMACDSignal(self, "close", 6, 13, 4, 6)
        elif signalId == 603:
            signal = entry.MACDHigherMACDSignal(self, "close", 12, 26, 9, 6)
        elif signalId == 604:
            signal = entry.MACDHigherMACDSignal(self, "close", 18, 39, 14, 6)

        elif signalId == 605:
            signal = entry.MACDHigherMACDSignal(self, "close", 6, 13, 4, 9)
        elif signalId == 606:
            signal = entry.MACDHigherMACDSignal(self, "close", 12, 26, 9, 9)
        elif signalId == 607:
            signal = entry.MACDHigherMACDSignal(self, "close", 18, 39, 14, )

        elif signalId == 608:
            signal = entry.MACDHigherMACDSignal(self, "close", 6, 13, 4, 12)
        elif signalId == 609:
            signal = entry.MACDHigherMACDSignal(self, "close", 12, 26, 9, 12)
        elif signalId == 610:
            signal = entry.MACDHigherMACDSignal(self, "close", 18, 39, 14, 12)
        # </editor-fold>

        # <editor-fold desc="# 53 Inter day MACD cross">
        elif signalId == 611:
            signal = entry.MACDHigherMACDSignal(self, "closeD", 6, 13, 4, 1)
        elif signalId == 612:
            signal = entry.MACDHigherMACDSignal(self, "closeD", 12, 26, 9, 1)
        elif signalId == 613:
            signal = entry.MACDHigherMACDSignal(self, "closeD", 18, 39, 14, 1)
        # </editor-fold>

        # <editor-fold desc="# 54 Intra day Stochastic cross">
        elif signalId == 614:
            signal = entry.StochasticSlowKHigherD(self, "close", 5, 3, 3)
        elif signalId == 615:
            signal = entry.StochasticSlowKLowerD(self, "close", 5, 3, 3)
        elif signalId == 616:
            signal = entry.StochasticSlowKHigherD(self, "close", 10, 6, 6)
        elif signalId == 617:
            signal = entry.StochasticSlowKLowerD(self, "close", 10, 6, 6)
        # </editor-fold>

        # <editor-fold desc="# 55 Intra day Stochastic cross with delay">
        elif signalId == 618:
            signal = entry.StochasticSlowKHigherD(self, "close", 5, 3, 3)
            signal = entry.StochasticSlowKHigherD(self, "close", 5, 3, 3, 2)
        elif signalId == 619:
            signal = entry.StochasticSlowKLowerD(self, "close", 5, 3, 3)
            signal = entry.StochasticSlowKLowerD(self, "close", 5, 3, 3, 2)
        elif signalId == 620:
            signal = entry.StochasticSlowKHigherD(self, "close", 10, 6, 6)
            signal = entry.StochasticSlowKHigherD(self, "close", 10, 6, 6, 2)
        elif signalId == 621:
            signal = entry.StochasticSlowKLowerD(self, "close", 10, 6, 6)
            signal = entry.StochasticSlowKLowerD(self, "close", 10, 6, 6, 2)


        elif signalId == 622:
            signal = entry.StochasticSlowKHigherD(self, "close", 5, 3, 3)
            signal = entry.StochasticSlowKHigherD(self, "close", 5, 3, 3, 4)
        elif signalId == 623:
            signal = entry.StochasticSlowKLowerD(self, "close", 5, 3, 3)
            signal = entry.StochasticSlowKLowerD(self, "close", 5, 3, 3, 4)
        elif signalId == 624:
            signal = entry.StochasticSlowKHigherD(self, "close", 10, 6, 6)
            signal = entry.StochasticSlowKHigherD(self, "close", 10, 6, 6, 4)
        elif signalId == 625:
            signal = entry.StochasticSlowKLowerD(self, "close", 10, 6, 6)
            signal = entry.StochasticSlowKLowerD(self, "close", 10, 6, 6, 4)


        elif signalId == 626:
            signal = entry.StochasticSlowKHigherD(self, "close", 5, 3, 3)
            signal = entry.StochasticSlowKHigherD(self, "close", 5, 3, 3, 6)
        elif signalId == 627:
            signal = entry.StochasticSlowKLowerD(self, "close", 5, 3, 3)
            signal = entry.StochasticSlowKLowerD(self, "close", 5, 3, 3, 6)
        elif signalId == 628:
            signal = entry.StochasticSlowKHigherD(self, "close", 10, 6, 6)
            signal = entry.StochasticSlowKHigherD(self, "close", 10, 6, 6, 6)
        elif signalId == 629:
            signal = entry.StochasticSlowKLowerD(self, "close", 10, 6, 6)
            signal = entry.StochasticSlowKLowerD(self, "close", 10, 6, 6, 6)


        elif signalId == 630:
            signal = entry.StochasticSlowKHigherD(self, "close", 5, 3, 3)
            signal = entry.StochasticSlowKHigherD(self, "close", 5, 3, 3, 8)
        elif signalId == 631:
            signal = entry.StochasticSlowKLowerD(self, "close", 5, 3, 3)
            signal = entry.StochasticSlowKLowerD(self, "close", 5, 3, 3, 8)
        elif signalId == 632:
            signal = entry.StochasticSlowKHigherD(self, "close", 10, 6, 6)
            signal = entry.StochasticSlowKHigherD(self, "close", 10, 6, 6, 8)
        elif signalId == 633:
            signal = entry.StochasticSlowKLowerD(self, "close", 10, 6, 6)
            signal = entry.StochasticSlowKLowerD(self, "close", 10, 6, 6, 8)
        # </editor-fold>

        # <editor-fold desc="# 56 Inter day Stochastic cross">
        elif signalId == 634:
            signal = entry.StochasticSlowKHigherD(self, "close", 5, 3, 3, 1)
        elif signalId == 635:
            signal = entry.StochasticSlowKLowerD(self, "close", 5, 3, 3, 1)
        elif signalId == 636:
            signal = entry.StochasticSlowKHigherD(self, "close", 10, 6, 6, 1)
        elif signalId == 637:
            signal = entry.StochasticSlowKLowerD(self, "close", 10, 6, 6, 1)
        # </editor-fold>

        # <editor-fold desc="# 57 Intra day Stochastic Fast cross">
        elif signalId == 638:
            signal = entry.StochasticFastKHigherD(self, "close", 5, 3)
        elif signalId == 639:
            signal = entry.StochasticFastKLowerD(self, "close", 5, 3)
        elif signalId == 640:
            signal = entry.StochasticFastKHigherD(self, "close", 10, 6)
        elif signalId == 641:
            signal = entry.StochasticFastKLowerD(self, "close", 10, 6)
        # </editor-fold>

        # <editor-fold desc="# 58 Intra day Stochastic Fast cross with delay and maintain">
        elif signalId == 642:
            signal = entry.StochasticFastKHigherD(self, "close", 5, 3 )
            signal = entry.StochasticFastKHigherD(self, "close", 5, 3, 2)
        elif signalId == 643:
            signal = entry.StochasticFastKLowerD(self, "close", 5, 3)
            signal = entry.StochasticFastKLowerD(self, "close", 5, 3, 2)
        elif signalId == 644:
            signal = entry.StochasticFastKHigherD(self, "close", 10, 6)
            signal = entry.StochasticFastKHigherD(self, "close", 10, 6, 2)
        elif signalId == 645:
            signal = entry.StochasticFastKLowerD(self, "close", 10, 6)
            signal = entry.StochasticFastKLowerD(self, "close", 10, 6, 2)

        elif signalId == 646:
            signal = entry.StochasticFastKHigherD(self, "close", 5, 3)
            signal = entry.StochasticFastKHigherD(self, "close", 5, 3, 4)
        elif signalId == 647:
            signal = entry.StochasticFastKLowerD(self, "close", 5, 3)
            signal = entry.StochasticFastKLowerD(self, "close", 5, 3, 4)
        elif signalId == 648:
            signal = entry.StochasticFastKHigherD(self, "close", 10, 6)
            signal = entry.StochasticFastKHigherD(self, "close", 10, 6, 4)
        elif signalId == 649:
            signal = entry.StochasticFastKLowerD(self, "close", 10, 6)
            signal = entry.StochasticFastKLowerD(self, "close", 10, 6, 4)

        elif signalId == 650:
            signal = entry.StochasticFastKHigherD(self, "close", 5, 3)
            signal = entry.StochasticFastKHigherD(self, "close", 5, 3, 6)
        elif signalId == 651:
            signal = entry.StochasticFastKLowerD(self, "close", 5, 3)
            signal = entry.StochasticFastKLowerD(self, "close", 5, 3, 6)
        elif signalId == 652:
            signal = entry.StochasticFastKHigherD(self, "close", 10, 6)
            signal = entry.StochasticFastKHigherD(self, "close", 10, 6, 6)
        elif signalId == 653:
            signal = entry.StochasticFastKLowerD(self, "close", 10, 6)
            signal = entry.StochasticFastKLowerD(self, "close", 10, 6, 6)

        elif signalId == 654:
            signal = entry.StochasticFastKHigherD(self, "close", 5, 3)
            signal = entry.StochasticFastKHigherD(self, "close", 5, 3, 8)
        elif signalId == 655:
            signal = entry.StochasticFastKLowerD(self, "close", 5, 3)
            signal = entry.StochasticFastKLowerD(self, "close", 5, 3, 8)
        elif signalId == 656:
            signal = entry.StochasticFastKHigherD(self, "close", 10, 6)
            signal = entry.StochasticFastKHigherD(self, "close", 10, 6, 8)
        elif signalId == 657:
            signal = entry.StochasticFastKLowerD(self, "close", 10, 6)
            signal = entry.StochasticFastKLowerD(self, "close", 10, 6, 8)
        # </editor-fold>

        # <editor-fold desc="# 59 Inter day Stochastic Fast cross">
        elif signalId == 658:
            signal = entry.StochasticFastKHigherD(self, "close", 5, 3, 1)
        elif signalId == 659:
            signal = entry.StochasticFastKLowerD(self, "close", 5, 3, 1)
        elif signalId == 660:
            signal = entry.StochasticFastKHigherD(self, "close", 10, 6, 1)
        elif signalId == 661:
            signal = entry.StochasticFastKLowerD(self, "close", 10, 6, 1)
        # </editor-fold>

        # <editor-fold desc="# 60 Intra day Stochastic Relative Strength Index cross">
        elif signalId == 662:
            signal = entry.StochasticRSIKHigherD(self, "close", 14, 5, 3)
        elif signalId == 663:
            signal = entry.StochasticRSIKLowerD(self, "close", 14, 5, 3)
        elif signalId == 664:
            signal = entry.StochasticRSIKHigherD(self, "close", 14, 10, 6)
        elif signalId == 665:
            signal = entry.StochasticRSIKLowerD(self, "close", 14, 10, 6)
        # </editor-fold>

        # <editor-fold desc="# 61 Intra day Stochastic Relative Strength Index cross with delay and maintain">
        elif signalId == 666:
            signal = entry.StochasticRSIKHigherD(self, "close", 14, 5, 3)
            signal = entry.StochasticRSIKHigherD(self, "close", 14, 5, 3, 3)
        elif signalId == 667:
            signal = entry.StochasticRSIKHigherD(self, "close", 14, 10, 6)
            signal = entry.StochasticRSIKHigherD(self, "close", 14, 10, 6, 3)
        elif signalId == 668:
            signal = entry.StochasticRSIKLowerD(self, "close", 14, 5, 3)
            signal = entry.StochasticRSIKLowerD(self, "close", 14, 5, 3, 6)
        elif signalId == 669:
            signal = entry.StochasticRSIKLowerD(self, "close", 14, 10, 6)
            signal = entry.StochasticRSIKLowerD(self, "close", 14, 10, 6, 6)
        elif signalId == 670:
            signal = entry.StochasticRSIKLowerD(self, "close", 14, 5, 3)
            signal = entry.StochasticRSIKLowerD(self, "close", 14, 5, 3, 12)
        elif signalId == 671:
            signal = entry.StochasticRSIKLowerD(self, "close", 14, 10, 6)
            signal = entry.StochasticRSIKLowerD(self, "close", 14, 10, 6, 12)
        # </editor-fold>

        # <editor-fold desc="# 62 Inter day Stochastic Relative Strength Index cross">
        elif signalId == 672:
            signal = entry.StochasticRSIKHigherD(self, "closeD", 14, 5, 3, 1)
        elif signalId == 673:
            signal = entry.StochasticRSIKLowerD(self, "closeD", 14, 5, 3, 1)
        elif signalId == 674:
            signal = entry.StochasticRSIKHigherD(self, "closeD", 14, 10, 6, 1)
        elif signalId == 675:
            signal = entry.StochasticRSIKLowerD(self, "closeD", 14, 10, 6, 1)
        # </editor-fold>

        # <editor-fold desc="# 63 Intra day Stochastic Higher than threshold">
        elif signalId == 676:
            signal = entry.StochasticSlowHigherThreshold(self, "close", 5, 3, 3, 80)
        elif signalId == 677:
            signal = entry.StochasticSlowHigherThreshold(self, "close", 10, 6, 6, 80)
        elif signalId == 678:
            signal = entry.StochasticSlowHigherThreshold(self, "close", 5, 3, 3, 20)
        elif signalId == 679:
            signal = entry.StochasticSlowHigherThreshold(self, "close", 10, 6, 6, 20)
        # </editor-fold>

        # <editor-fold desc="# 64 Intra day Stochastic Higher than threshold with delay">
        elif signalId == 680:
            signal = entry.StochasticSlowHigherThreshold(self, "close", 5, 3, 3, 80, 3)
        elif signalId == 681:
            signal = entry.StochasticSlowHigherThreshold(self, "close", 10, 6, 6, 80, 3)
        elif signalId == 682:
            signal = entry.StochasticSlowHigherThreshold(self, "close", 5, 3, 3, 20, 6)
        elif signalId == 683:
            signal = entry.StochasticSlowHigherThreshold(self, "close", 10, 6, 6, 20, 6)
        elif signalId == 684:
            signal = entry.StochasticSlowHigherThreshold(self, "close", 5, 3, 3, 20, 12)
        elif signalId == 685:
            signal = entry.StochasticSlowHigherThreshold(self, "close", 10, 6, 6, 20, 12)
        # </editor-fold>

        # <editor-fold desc="# 65 Inter day Stochastic Higher than threshold">
        elif signalId == 686:
            signal = entry.StochasticSlowHigherThreshold(self, "closeD", 5, 3, 3, 20, 1)
        elif signalId == 687:
            signal = entry.StochasticSlowHigherThreshold(self, "closeD", 5, 3, 3, 80, 1)
        # </editor-fold>

        # <editor-fold desc="# 66 Intra day Stochastic Lower than threshold">
        elif signalId == 688:
            signal = entry.StochasticSlowLowerThreshold(self, "close", 5, 3, 3, 80)
        elif signalId == 689:
            signal = entry.StochasticSlowLowerThreshold(self, "close", 10, 6, 6, 80)
        elif signalId == 690:
            signal = entry.StochasticSlowLowerThreshold(self, "close", 5, 3, 3, 20)
        elif signalId == 691:
            signal = entry.StochasticSlowLowerThreshold(self, "close", 10, 6, 6, 20)
        # </editor-fold>

        # <editor-fold desc="# 67 Intra day Stochastic Lower than threshold with delay">
        elif signalId == 692:
            signal = entry.StochasticSlowLowerThreshold(self, "close", 5, 3, 3, 80, 3)
        elif signalId == 693:
            signal = entry.StochasticSlowLowerThreshold(self, "close", 10, 6, 6, 80, 3)
        elif signalId == 694:
            signal = entry.StochasticSlowLowerThreshold(self, "close", 5, 3, 3, 20, 6)
        elif signalId == 695:
            signal = entry.StochasticSlowLowerThreshold(self, "close", 10, 6, 6, 20, 6)
        elif signalId == 696:
            signal = entry.StochasticSlowLowerThreshold(self, "close", 5, 3, 3, 20, 12)
        elif signalId == 697:
            signal = entry.StochasticSlowLowerThreshold(self, "close", 10, 6, 6, 20, 12)
        # </editor-fold>

        # <editor-fold desc="# 68 Inter day Stochastic Lower than threshold">
        elif signalId == 698:
            signal = entry.StochasticSlowLowerThreshold(self, "closeD", 5, 3, 3, 20, 1)
        elif signalId == 699:
            signal = entry.StochasticSlowLowerThreshold(self, "closeD", 5, 3, 3, 80, 1)
        # </editor-fold>

        # <editor-fold desc="# 69 Intra day Stochastic fast Higher than threshold">
        elif signalId == 700:
            signal = entry.StochasticFastHigherThreshold(self, "close", 5, 3, 80)
        elif signalId == 701:
            signal = entry.StochasticFastHigherThreshold(self, "close", 10, 6, 80)
        elif signalId == 702:
            signal = entry.StochasticFastHigherThreshold(self, "close", 5, 3, 20)
        elif signalId == 703:
            signal = entry.StochasticFastHigherThreshold(self, "close", 10, 6, 20)
        # </editor-fold>

        # <editor-fold desc="# 70 Intra day Stochastic fast Higher than threshold with delay">
        elif signalId == 704:
            signal = entry.StochasticFastHigherThreshold(self, "close", 5, 3, 80, 2)
        elif signalId == 705:
            signal = entry.StochasticFastHigherThreshold(self, "close", 10, 6, 80, 2)
        elif signalId == 706:
            signal = entry.StochasticFastHigherThreshold(self, "close", 5, 3, 20, 4)
        elif signalId == 707:
            signal = entry.StochasticFastHigherThreshold(self, "close", 10, 6, 20, 4)
        elif signalId == 708:
            signal = entry.StochasticFastHigherThreshold(self, "close", 5, 3, 20, 6)
        elif signalId == 709:
            signal = entry.StochasticFastHigherThreshold(self, "close", 10, 6, 20, 6)
        # </editor-fold>

        # <editor-fold desc="# 71 Inter day Stochastic fast Higher than threshold">
        elif signalId == 710:
            signal = entry.StochasticFastHigherThreshold(self, "closeD", 5, 3, 20, 1)
        elif signalId == 711:
            signal = entry.StochasticFastHigherThreshold(self, "closeD", 5, 3, 80, 1)
        # </editor-fold>

        # <editor-fold desc="# 72 Intra day Stochastic fast Lower than threshold">
        elif signalId == 712:
            signal = entry.StochasticFastLowerThreshold(self, "close", 5, 3, 80)
        elif signalId == 713:
            signal = entry.StochasticFastLowerThreshold(self, "close", 10, 6, 80)
        elif signalId == 714:
            signal = entry.StochasticFastLowerThreshold(self, "close", 5, 3, 20)
        elif signalId == 715:
            signal = entry.StochasticFastLowerThreshold(self, "close", 10, 6, 20)
        # </editor-fold>

        # <editor-fold desc="# 73 Intra day Stochastic fast Lower than threshold with delay">
        elif signalId == 716:
            signal = entry.StochasticFastLowerThreshold(self, "close", 5, 3, 80, 2)
        elif signalId == 717:
            signal = entry.StochasticFastLowerThreshold(self, "close", 10, 6, 80, 2)
        elif signalId == 718:
            signal = entry.StochasticFastLowerThreshold(self, "close", 5, 3, 20, 4)
        elif signalId == 719:
            signal = entry.StochasticFastLowerThreshold(self, "close", 10, 6, 20, 4)
        elif signalId == 720:
            signal = entry.StochasticFastLowerThreshold(self, "close", 5, 3, 20, 6)
        elif signalId == 721:
            signal = entry.StochasticFastLowerThreshold(self, "close", 10, 6, 20, 6)
        # </editor-fold>

        # <editor-fold desc="# 74 Inter day Stochastic fast Lower than threshold">
        elif signalId == 722:
            signal = entry.StochasticFastLowerThreshold(self, "closeD", 5, 3, 20, 1)
        elif signalId == 723:
            signal = entry.StochasticFastLowerThreshold(self, "closeD", 5, 3, 80, 1)
        # </editor-fold>

        # <editor-fold desc="# 75 Intra day Stochastic RSI Higher than threshold">
        elif signalId == 724:
            signal = entry.StochasticRSIHigherThreshold(self, "close", 14, 5, 3, 80)
        elif signalId == 725:
            signal = entry.StochasticRSIHigherThreshold(self, "close", 14, 10, 6, 80)
        elif signalId == 726:
            signal = entry.StochasticRSIHigherThreshold(self, "close", 14, 5, 3, 20)
        elif signalId == 727:
            signal = entry.StochasticRSIHigherThreshold(self, "close", 14, 10, 6, 20)
        # </editor-fold>

        # <editor-fold desc="# 76 Intra day Stochastic RSI Higher than threshold with delay">
        elif signalId == 728:
            signal = entry.StochasticRSIHigherThreshold(self, "close", 14, 5, 3, 80, 2)
        elif signalId == 729:
            signal = entry.StochasticRSIHigherThreshold(self, "close", 14, 10, 6, 80, 2)
        elif signalId == 730:
            signal = entry.StochasticRSIHigherThreshold(self, "close", 14, 5, 3, 20, 4)
        elif signalId == 731:
            signal = entry.StochasticRSIHigherThreshold(self, "close", 14, 10, 6, 20, 4)
        elif signalId == 732:
            signal = entry.StochasticRSIHigherThreshold(self, "close", 14, 5, 3, 20, 6)
        elif signalId == 733:
            signal = entry.StochasticRSIHigherThreshold(self, "close", 14, 10, 6, 20, 6)
        # </editor-fold>

        # <editor-fold desc="# 77 Inter day Stochastic RSI Higher than threshold">
        elif signalId == 734:
            signal = entry.StochasticRSIHigherThreshold(self, "closeD", 14, 5, 3, 20, 1)
        elif signalId == 735:
            signal = entry.StochasticRSIHigherThreshold(self, "closeD", 14, 5, 3, 80, 1)
        # </editor-fold>

        # <editor-fold desc="# 78 Intra day Stochastic RSI Lower than threshold">
        elif signalId == 736:
            signal = entry.StochasticRSILowerThreshold(self, "close", 14, 5, 3, 80)
        elif signalId == 737:
            signal = entry.StochasticRSILowerThreshold(self, "close", 14, 10, 6, 80)
        elif signalId == 738:
            signal = entry.StochasticRSILowerThreshold(self, "close", 14, 5, 3, 20)
        elif signalId == 739:
            signal = entry.StochasticRSILowerThreshold(self, "close", 14, 10, 6, 20)
        # </editor-fold>

        # <editor-fold desc="# 79 Intra day Stochastic RSI Lower than threshold with delay">
        elif signalId == 740:
            signal = entry.StochasticRSILowerThreshold(self, "close", 14, 5, 3, 80, 2)
        elif signalId == 741:
            signal = entry.StochasticRSILowerThreshold(self, "close", 14, 10, 6, 80, 2)
        elif signalId == 742:
            signal = entry.StochasticRSILowerThreshold(self, "close", 14, 5, 3, 20, 4)
        elif signalId == 743:
            signal = entry.StochasticRSILowerThreshold(self, "close", 14, 10, 6, 20, 4)
        elif signalId == 744:
            signal = entry.StochasticRSILowerThreshold(self, "close", 14, 5, 3, 20, 6)
        elif signalId == 745:
            signal = entry.StochasticRSILowerThreshold(self, "close", 14, 10, 6, 20, 6)
        # </editor-fold>

        # <editor-fold desc="# 80 Inter day Stochastic RSI Lower than threshold">
        elif signalId == 746:
            signal = entry.StochasticRSILowerThreshold(self, "closeD", 14, 5, 3, 20, 1)
        elif signalId == 747:
            signal = entry.StochasticRSILowerThreshold(self, "closeD", 14, 5, 3, 80, 1)
        # </editor-fold>

        # <editor-fold desc="# 81 Intra day Higher KAMA">
        elif signalId == 748:
            signal = entry.XHigherKAMA(self, "close", 0, 10)
        elif signalId == 749:
            signal = entry.XHigherKAMA(self, "close", 0, 20)
        elif signalId == 750:
            signal = entry.XHigherKAMA(self, "close", 0, 30)
        elif signalId == 751:
            signal = entry.XHigherKAMA(self, "close", 0, 40)
        # </editor-fold>

        # <editor-fold desc="# 82 Intra day Higher KAMA with delay">
        elif signalId == 752:
            signal = entry.XHigherKAMA(self, "close", 3, 10, 3)
        elif signalId == 753:
            signal = entry.XHigherKAMA(self, "close", 3, 20, 3)
        elif signalId == 754:
            signal = entry.XHigherKAMA(self, "close", 3, 30, 3)
        elif signalId == 755:
            signal = entry.XHigherKAMA(self, "close", 3, 40, 3)

        elif signalId == 756:
            signal = entry.XHigherKAMA(self, "close", 6, 10, 6)
        elif signalId == 757:
            signal = entry.XHigherKAMA(self, "close", 6, 20, 6)
        elif signalId == 758:
            signal = entry.XHigherKAMA(self, "close", 6, 30, 6)
        elif signalId == 759:
            signal = entry.XHigherKAMA(self, "close", 6, 40, 6)

        elif signalId == 760:
            signal = entry.XHigherKAMA(self, "close", 9, 10, 9)
        elif signalId == 761:
            signal = entry.XHigherKAMA(self, "close", 9, 20, 9)
        elif signalId == 762:
            signal = entry.XHigherKAMA(self, "close", 9, 30, 9)
        elif signalId == 763:
            signal = entry.XHigherKAMA(self, "close", 9, 40, 9)

        elif signalId == 764:
            signal = entry.XHigherKAMA(self, "close", 12, 10, 12)
        elif signalId == 765:
            signal = entry.XHigherKAMA(self, "close", 12, 20, 12)
        elif signalId == 766:
            signal = entry.XHigherKAMA(self, "close", 12, 30, 12)
        elif signalId == 767:
            signal = entry.XHigherKAMA(self, "close", 12, 40, 12)
        # </editor-fold>

        # <editor-fold desc="# 83 Intra day Higher KAMA with delay and maintain">
        elif signalId == 768:
            signal = entry.XHigherKAMA(self, "close", 0, 10)
            signal = entry.XHigherKAMA(self, "close", 3, 10, 3)
        elif signalId == 769:
            signal = entry.XHigherKAMA(self, "close", 0, 20)
            signal = entry.XHigherKAMA(self, "close", 3, 20, 3)
        elif signalId == 770:
            signal = entry.XHigherKAMA(self, "close", 0, 30)
            signal = entry.XHigherKAMA(self, "close", 3, 30, 3)
        elif signalId == 771:
            signal = entry.XHigherKAMA(self, "close", 0, 40)
            signal = entry.XHigherKAMA(self, "close", 3, 40, 3)

        elif signalId == 772:
            signal = entry.XHigherKAMA(self, "close", 0, 10)
            signal = entry.XHigherKAMA(self, "close", 6, 10, 6)
        elif signalId == 773:
            signal = entry.XHigherKAMA(self, "close", 0, 20)
            signal = entry.XHigherKAMA(self, "close", 6, 20, 6)
        elif signalId == 774:
            signal = entry.XHigherKAMA(self, "close", 0, 30)
            signal = entry.XHigherKAMA(self, "close", 6, 30, 6)
        elif signalId == 775:
            signal = entry.XHigherKAMA(self, "close", 0, 40)
            signal = entry.XHigherKAMA(self, "close", 6, 40, 6)

        elif signalId == 776:
            signal = entry.XHigherKAMA(self, "close", 0, 10)
            signal = entry.XHigherKAMA(self, "close", 9, 10, 9)
        elif signalId == 777:
            signal = entry.XHigherKAMA(self, "close", 0, 20)
            signal = entry.XHigherKAMA(self, "close", 9, 20, 9)
        elif signalId == 778:
            signal = entry.XHigherKAMA(self, "close", 0, 30)
            signal = entry.XHigherKAMA(self, "close", 9, 30, 9)
        elif signalId == 779:
            signal = entry.XHigherKAMA(self, "close", 0, 40)
            signal = entry.XHigherKAMA(self, "close", 9, 40, 9)

        elif signalId == 780:
            signal = entry.XHigherKAMA(self, "close", 0, 10)
            signal = entry.XHigherKAMA(self, "close", 12, 10, 12)
        elif signalId == 781:
            signal = entry.XHigherKAMA(self, "close", 0, 20)
            signal = entry.XHigherKAMA(self, "close", 12, 20, 12)
        elif signalId == 782:
            signal = entry.XHigherKAMA(self, "close", 0, 30)
            signal = entry.XHigherKAMA(self, "close", 12, 30, 12)
        elif signalId == 783:
            signal = entry.XHigherKAMA(self, "close", 0, 40)
            signal = entry.XHigherKAMA(self, "close", 12, 40, 12)
        # </editor-fold>

        # <editor-fold desc="# 84 Inter day Higher KAMA">
        elif signalId == 784:
            signal = entry.XHigherKAMA(self, "closeD", 1, 10, 1)
        elif signalId == 785:
            signal = entry.XHigherKAMA(self, "closeD", 1, 20, 1)
        elif signalId == 786:
            signal = entry.XHigherKAMA(self, "closeD", 1, 30, 1)
        elif signalId == 787:
            signal = entry.XHigherKAMA(self, "closeD", 1, 40, 1)
        elif signalId == 788:
            signal = entry.XHigherKAMA(self, "closeD", 1, 50, 1)
        # </editor-fold>

        # <editor-fold desc="# 85 Intra day in BBANDS Zone">
        elif signalId == 789:
            signal = entry.XHigherBBandsUpper(self, "close", 20, 2)
        elif signalId == 790:
            signal = entry.XLowerBBandsUpper(self, "close", 20, 2)
            signal = entry.XHigherBBandsMiddle(self, "close", 20, 2)
        elif signalId == 791:
            signal = entry.XLowerBBandsMiddle(self, "close", 20, 2)
            signal = entry.XHigherBBandsLower(self, "close", 20, 2)
        elif signalId == 792:
            signal = entry.XLowerBBandsLower(self, "close", 20, 2)
        # </editor-fold>

        # <editor-fold desc="# 86 Intra day Higher BBANDS with delay">
        elif signalId == 793:
            signal = entry.XHigherBBandsUpper(self, "close", 20, 2)
            signal = entry.XHigherBBandsUpper(self, "close", 20, 2, 3, 3)
        elif signalId == 794:
            signal = entry.XLowerBBandsUpper(self, "close", 20, 2)
            signal = entry.XHigherBBandsMiddle(self, "close", 20, 2)
            signal = entry.XLowerBBandsUpper(self, "close", 20, 2, 3, 3)
            signal = entry.XHigherBBandsMiddle(self, "close", 20, 2, 3, 3)
        elif signalId == 795:
            signal = entry.XLowerBBandsMiddle(self, "close", 20, 2)
            signal = entry.XHigherBBandsLower(self, "close", 20, 2)
            signal = entry.XLowerBBandsMiddle(self, "close", 20, 2, 3, 3)
            signal = entry.XHigherBBandsLower(self, "close", 20, 2, 3, 3)
        elif signalId == 796:
            signal = entry.XLowerBBandsLower(self, "close", 20, 2)
            signal = entry.XLowerBBandsLower(self, "close", 20, 2, 3, 3)


        elif signalId == 797:
            signal = entry.XHigherBBandsUpper(self, "close", 20, 2)
            signal = entry.XHigherBBandsUpper(self, "close", 20, 2, 6, 6)
        elif signalId == 798:
            signal = entry.XLowerBBandsUpper(self, "close", 20, 2)
            signal = entry.XHigherBBandsMiddle(self, "close", 20, 2)
            signal = entry.XLowerBBandsUpper(self, "close", 20, 2, 6, 6)
            signal = entry.XHigherBBandsMiddle(self, "close", 20, 2, 6, 6)
        elif signalId == 799:
            signal = entry.XLowerBBandsMiddle(self, "close", 20, 2)
            signal = entry.XHigherBBandsLower(self, "close", 20, 2)
            signal = entry.XLowerBBandsMiddle(self, "close", 20, 2, 6, 6)
            signal = entry.XHigherBBandsLower(self, "close", 20, 2, 6, 6)
        elif signalId == 800:
            signal = entry.XLowerBBandsLower(self, "close", 20, 2)
            signal = entry.XLowerBBandsLower(self, "close", 20, 2, 6, 6)


        elif signalId == 801:
            signal = entry.XHigherBBandsUpper(self, "close", 20, 2)
            signal = entry.XHigherBBandsUpper(self, "close", 20, 2, 12, 12)
        elif signalId == 802:
            signal = entry.XLowerBBandsUpper(self, "close", 20, 2)
            signal = entry.XHigherBBandsMiddle(self, "close", 20, 2)
            signal = entry.XLowerBBandsUpper(self, "close", 20, 2, 12, 12)
            signal = entry.XHigherBBandsMiddle(self, "close", 20, 2, 12, 12)
        elif signalId == 803:
            signal = entry.XLowerBBandsMiddle(self, "close", 20, 2)
            signal = entry.XHigherBBandsLower(self, "close", 20, 2)
            signal = entry.XLowerBBandsMiddle(self, "close", 20, 2, 12, 12)
            signal = entry.XHigherBBandsLower(self, "close", 20, 2, 12, 12)
        elif signalId == 804:
            signal = entry.XLowerBBandsLower(self, "close", 20, 2)
            signal = entry.XLowerBBandsLower(self, "close", 20, 2, 12, 12)
        # </editor-fold>

        # <editor-fold desc="# 87 Inter day in BBANDS Zone">
        elif signalId == 805:
            signal = entry.XHigherBBandsUpper(self, "closeD", 20, 2, 1, 1)
        elif signalId == 806:
            signal = entry.XLowerBBandsUpper(self, "closeD", 20, 2, 1, 1)
            signal = entry.XHigherBBandsMiddle(self, "closeD", 20, 2, 1, 1)
        elif signalId == 807:
            signal = entry.XLowerBBandsMiddle(self, "closeD", 20, 2, 1, 1)
            signal = entry.XHigherBBandsLower(self, "closeD", 20, 2, 1, 1)
        elif signalId == 808:
            signal = entry.XLowerBBandsLower(self, "closeD", 20, 2, 1, 1)
        # </editor-fold>

        # <editor-fold desc="# 88 Inter day BBANDS width change">
        elif signalId == 809:
            signal = entry.NarrowerBBands(self, "close", 20, 2, 0, 3, 0.6)
        elif signalId == 810:
            signal = entry.NarrowerBBands(self, "close", 20, 2, 0, 6, 0.6)
        elif signalId == 811:
            signal = entry.NarrowerBBands(self, "close", 20, 2, 0, 9, 0.6)
        elif signalId == 812:
            signal = entry.NarrowerBBands(self, "close", 20, 2, 0, 12, 0.6)
        elif signalId == 813:
            signal = entry.NarrowerBBands(self, "close", 20, 2, 0, 3, 0.8)
        elif signalId == 814:
            signal = entry.NarrowerBBands(self, "close", 20, 2, 0, 6, 0.8)
        elif signalId == 815:
            signal = entry.NarrowerBBands(self, "close", 20, 2, 0, 9, 0.8)
        elif signalId == 816:
            signal = entry.NarrowerBBands(self, "close", 20, 2, 0, 12, 0.8)

        elif signalId == 817:
            signal = entry.WiderBBands(self, "close", 20, 2, 0, 3, 1.2)
        elif signalId == 818:
            signal = entry.WiderBBands(self, "close", 20, 2, 0, 6, 1.2)
        elif signalId == 819:
            signal = entry.WiderBBands(self, "close", 20, 2, 0, 9, 1.2)
        elif signalId == 820:
            signal = entry.WiderBBands(self, "close", 20, 2, 0, 12, 1.2)
        elif signalId == 821:
            signal = entry.WiderBBands(self, "close", 20, 2, 0, 3, 1.4)
        elif signalId == 822:
            signal = entry.WiderBBands(self, "close", 20, 2, 0, 6, 1.4)
        elif signalId == 823:
            signal = entry.WiderBBands(self, "close", 20, 2, 0, 9, 1.4)
        elif signalId == 824:
            signal = entry.WiderBBands(self, "close", 20, 2, 0, 12, 1.4)
        # </editor-fold>

        # <editor-fold desc="# 89 Higher previous Day high with threshold">
        elif signalId == 825:
            signal = entry.XHigherYWithThresold(self, "close", 0, "highD", 1, 0, 0, 80)
        elif signalId == 826:
            signal = entry.XHigherYWithThresold(self, "close", 0, "highD", 1, 0, 0, 120)
        elif signalId == 827:
            signal = entry.XHigherYWithThresold(self, "close", 0, "highD", 1, 0, 0, 160)
        # </editor-fold>

        # <editor-fold desc="# 90 Higher current Day low with threshold">
        elif signalId == 828:
            signal = entry.XHigherYWithThresold(self, "close", 0, "lowD", 0, 0, 0, 80)
        elif signalId == 829:
            signal = entry.XHigherYWithThresold(self, "close", 0, "lowD", 0, 0, 0, 120)
        elif signalId == 830:
            signal = entry.XHigherYWithThresold(self, "close", 0, "lowD", 0, 0, 0, 160)
        elif signalId == 831:
            signal = entry.XHigherYWithThresold(self, "close", 0, "lowD", 0, 0, 0, 200)
        elif signalId == 832:
            signal = entry.XHigherYWithThresold(self, "close", 0, "lowD", 0, 0, 0, 240)
        elif signalId == 833:
            signal = entry.XHigherYWithThresold(self, "close", 0, "lowD", 0, 0, 0, 280)
        # </editor-fold>

        # <editor-fold desc="# 91 Higher current Day low with threshold with delay">
        elif signalId == 834:
            signal = entry.XHigherYWithThresold(self, "close", 3, "lowD", 0, 0, 0, 80)
        elif signalId == 835:
            signal = entry.XHigherYWithThresold(self, "close", 6, "lowD", 0, 0, 0, 80)
        elif signalId == 836:
            signal = entry.XHigherYWithThresold(self, "close", 12, "lowD", 0, 0, 0, 80)

        elif signalId == 837:
            signal = entry.XHigherYWithThresold(self, "close", 3, "lowD", 0, 0, 0, 120)
        elif signalId == 838:
            signal = entry.XHigherYWithThresold(self, "close", 6, "lowD", 0, 0, 0, 120)
        elif signalId == 839:
            signal = entry.XHigherYWithThresold(self, "close", 12, "lowD", 0, 0, 0, 120)

        elif signalId == 840:
            signal = entry.XHigherYWithThresold(self, "close", 3, "lowD", 0, 0, 0, 160)
        elif signalId == 841:
            signal = entry.XHigherYWithThresold(self, "close", 6, "lowD", 0, 0, 0, 160)
        elif signalId == 842:
            signal = entry.XHigherYWithThresold(self, "close", 12, "lowD", 0, 0, 0, 160)

        elif signalId == 843:
            signal = entry.XHigherYWithThresold(self, "close", 3, "lowD", 0, 0, 0, 200)
        elif signalId == 844:
            signal = entry.XHigherYWithThresold(self, "close", 6, "lowD", 0, 0, 0, 200)
        elif signalId == 845:
            signal = entry.XHigherYWithThresold(self, "close", 12, "lowD", 0, 0, 0, 200)

        elif signalId == 846:
            signal = entry.XHigherYWithThresold(self, "close", 3, "lowD", 0, 0, 0, 240)
        elif signalId == 847:
            signal = entry.XHigherYWithThresold(self, "close", 6, "lowD", 0, 0, 0, 240)
        elif signalId == 848:
            signal = entry.XHigherYWithThresold(self, "close", 12, "lowD", 0, 0, 0, 240)

        elif signalId == 849:
            signal = entry.XHigherYWithThresold(self, "close", 3, "lowD", 0, 0, 0, 280)
        elif signalId == 850:
            signal = entry.XHigherYWithThresold(self, "close", 6, "lowD", 0, 0, 0, 280)
        elif signalId == 851:
            signal = entry.XHigherYWithThresold(self, "close", 12, "lowD", 0, 0, 0, 280)
        # </editor-fold>

        # <editor-fold desc="# 92 Lower current day high with threshold">
        elif signalId == 852:
            signal = entry.XLowerYWithThresold(self, "close", 0, "highD", 0, 0, 0, 80)
        elif signalId == 853:
            signal = entry.XLowerYWithThresold(self, "close", 0, "highD", 0, 0, 0, 120)
        elif signalId == 854:
            signal = entry.XLowerYWithThresold(self, "close", 0, "highD", 0, 0, 0, 160)
        elif signalId == 855:
            signal = entry.XLowerYWithThresold(self, "close", 0, "highD", 0, 0, 0, 200)
        elif signalId == 856:
            signal = entry.XLowerYWithThresold(self, "close", 0, "highD", 0, 0, 0, 240)
        elif signalId == 857:
            signal = entry.XLowerYWithThresold(self, "close", 0, "highD", 0, 0, 0, 280)
        # </editor-fold>

        # <editor-fold desc="# 93 Lower current day high with threshold with delay">
        elif signalId == 858:
            signal = entry.XLowerYWithThresold(self, "close", 3, "highD", 0, 0, 0, 80)
        elif signalId == 859:
            signal = entry.XLowerYWithThresold(self, "close", 6, "highD", 0, 0, 0, 80)
        elif signalId == 860:
            signal = entry.XLowerYWithThresold(self, "close", 12, "highD", 0, 0, 0, 80)

        elif signalId == 861:
            signal = entry.XLowerYWithThresold(self, "close", 3, "highD", 0, 0, 0, 120)
        elif signalId == 862:
            signal = entry.XLowerYWithThresold(self, "close", 6, "highD", 0, 0, 0, 120)
        elif signalId == 863:
            signal = entry.XLowerYWithThresold(self, "close", 12, "highD", 0, 0, 0, 120)

        elif signalId == 864:
            signal = entry.XLowerYWithThresold(self, "close", 3, "highD", 0, 0, 0, 160)
        elif signalId == 865:
            signal = entry.XLowerYWithThresold(self, "close", 6, "highD", 0, 0, 0, 160)
        elif signalId == 866:
            signal = entry.XLowerYWithThresold(self, "close", 12, "highD", 0, 0, 0, 160)

        elif signalId == 867:
            signal = entry.XLowerYWithThresold(self, "close", 3, "highD", 0, 0, 0, 200)
        elif signalId == 868:
            signal = entry.XLowerYWithThresold(self, "close", 6, "highD", 0, 0, 0, 200)
        elif signalId == 869:
            signal = entry.XLowerYWithThresold(self, "close", 12, "highD", 0, 0, 0, 200)

        elif signalId == 870:
            signal = entry.XLowerYWithThresold(self, "close", 3, "highD", 0, 0, 0, 240)
        elif signalId == 871:
            signal = entry.XLowerYWithThresold(self, "close", 6, "highD", 0, 0, 0, 240)
        elif signalId == 872:
            signal = entry.XLowerYWithThresold(self, "close", 12, "highD", 0, 0, 0, 240)

        elif signalId == 873:
            signal = entry.XLowerYWithThresold(self, "close", 3, "highD", 0, 0, 0, 280)
        elif signalId == 874:
            signal = entry.XLowerYWithThresold(self, "close", 6, "highD", 0, 0, 0, 280)
        elif signalId == 875:
            signal = entry.XLowerYWithThresold(self, "close", 12, "highD", 0, 0, 0, 280)
        # </editor-fold>




        # <editor-fold desc="# 94 current day range larger than threshold">
        elif signalId == 876:
            signal = entry.XYRangeLargerThresold(self, "highD", 0, "lowD", 0, 80)
        elif signalId == 877:
            signal = entry.XYRangeLargerThresold(self, "highD", 0, "lowD", 0, 160)
        elif signalId == 878:
            signal = entry.XYRangeLargerThresold(self, "highD", 0, "lowD", 0, 240)
        elif signalId == 879:
            signal = entry.XYRangeLargerThresold(self, "highD", 0, "lowD", 0, 320)
        # </editor-fold>

        # <editor-fold desc="# 95 current day range smaller than threshold">
        elif signalId == 880:
            signal = entry.XYRangeSmallerThresold(self, "highD", 0, "lowD", 0, 80)
        elif signalId == 881:
            signal = entry.XYRangeSmallerThresold(self, "highD", 0, "lowD", 0, 160)
        elif signalId == 882:
            signal = entry.XYRangeSmallerThresold(self, "highD", 0, "lowD", 0, 240)
        elif signalId == 883:
            signal = entry.XYRangeSmallerThresold(self, "highD", 0, "lowD", 0, 320)
        # </editor-fold>


        # <editor-fold desc="# 96 previous day range larger 2 previous day range">
        elif signalId == 884:
            signal = entry.XYRangeSmallerThresold(self, "highD", 2, "lowD", 2, 150)
            signal = entry.XYRangeLargerThresold(self, "highD", 1, "lowD", 1, 250)
        elif signalId == 885:
            signal = entry.XYRangeSmallerThresold(self, "highD", 2, "lowD", 2, 250)
            signal = entry.XYRangeLargerThresold(self, "highD", 1, "lowD", 1, 350)
        elif signalId == 886:
            signal = entry.XYRangeSmallerThresold(self, "highD", 2, "lowD", 2, 350)
            signal = entry.XYRangeLargerThresold(self, "highD", 1, "lowD", 1, 450)
        # </editor-fold>


        # <editor-fold desc="# 97 previous day range with threshold">
        elif signalId == 887:
            signal = entry.XYRangeSmallerThresold(self, "highD", 1, "lowD", 1, 100)
        elif signalId == 888:
            signal = entry.XYRangeSmallerThresold(self, "highD", 1, "lowD", 1, 200)
        elif signalId == 889:
            signal = entry.XYRangeSmallerThresold(self, "highD", 1, "lowD", 1, 300)
        elif signalId == 890:
            signal = entry.XYRangeSmallerThresold(self, "highD", 1, "lowD", 1, 400)

        elif signalId == 891:
            signal = entry.XYRangeSmallerThresold(self, "highD", 2, "lowD", 2, 100)
        elif signalId == 892:
            signal = entry.XYRangeSmallerThresold(self, "highD", 2, "lowD", 2, 200)
        elif signalId == 893:
            signal = entry.XYRangeSmallerThresold(self, "highD", 2, "lowD", 2, 300)
        elif signalId == 894:
            signal = entry.XYRangeSmallerThresold(self, "highD", 2, "lowD", 2, 400)

        elif signalId == 895:
            signal = entry.XYRangeSmallerThresold(self, "highD", 3, "lowD", 3, 100)
        elif signalId == 896:
            signal = entry.XYRangeSmallerThresold(self, "highD", 3, "lowD", 3, 200)
        elif signalId == 897:
            signal = entry.XYRangeSmallerThresold(self, "highD", 3, "lowD", 3, 300)
        elif signalId == 898:
            signal = entry.XYRangeSmallerThresold(self, "highD", 3, "lowD", 3, 400)

        elif signalId == 899:
            signal = entry.XYRangeLargerThresold(self, "highD", 1, "lowD", 1, 100)
        elif signalId == 900:
            signal = entry.XYRangeLargerThresold(self, "highD", 1, "lowD", 1, 200)
        elif signalId == 901:
            signal = entry.XYRangeLargerThresold(self, "highD", 1, "lowD", 1, 300)
        elif signalId == 902:
            signal = entry.XYRangeLargerThresold(self, "highD", 1, "lowD", 1, 400)

        elif signalId == 903:
            signal = entry.XYRangeLargerThresold(self, "highD", 2, "lowD", 2, 100)
        elif signalId == 903:
            signal = entry.XYRangeLargerThresold(self, "highD", 2, "lowD", 2, 200)
        elif signalId == 905:
            signal = entry.XYRangeLargerThresold(self, "highD", 2, "lowD", 2, 300)
        elif signalId == 906:
            signal = entry.XYRangeLargerThresold(self, "highD", 2, "lowD", 2, 400)

        elif signalId == 907:
            signal = entry.XYRangeLargerThresold(self, "highD", 3, "lowD", 3, 100)
        elif signalId == 908:
            signal = entry.XYRangeLargerThresold(self, "highD", 3, "lowD", 3, 200)
        elif signalId == 909:
            signal = entry.XYRangeLargerThresold(self, "highD", 3, "lowD", 3, 300)
        elif signalId == 910:
            signal = entry.XYRangeLargerThresold(self, "highD", 3, "lowD", 3, 400)
        # </editor-fold>


        # <editor-fold desc="# 98 previous day period close compare">
        elif signalId == 911:
            signal = entry.XHigherY(self, "afternoonCloseD", 1, "openD", 1)
        elif signalId == 912:
            signal = entry.XHigherY(self, "athCloseD", 1, "afternoonCloseD", 1)
        elif signalId == 913:
            signal = entry.XHigherY(self, "afternoonCloseD", 1, "openD", 1)
            signal = entry.XHigherY(self, "athCloseD", 1, "afternoonCloseD", 1)

        elif signalId == 914:
            signal = entry.XLowerY(self, "afternoonCloseD", 1, "openD", 1)
        elif signalId == 915:
            signal = entry.XLowerY(self, "athCloseD", 1, "afternoonCloseD", 1)
        elif signalId == 916:
            signal = entry.XLowerY(self, "afternoonCloseD", 1, "openD", 1)
            signal = entry.XLowerY(self, "athCloseD", 1, "afternoonCloseD", 1)
        # </editor-fold>
