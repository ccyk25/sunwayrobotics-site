
# ---------- logo geometry ----------
SQ = [(467, 141), (533, 141), (533, 213), (467, 213)]
URT = [(442, 239), (560, 239), (560, 319)]
LLT = [(442, 281), (442, 359), (559, 359)]
DEPTH = 0.22; YP = -0.32                      # parts plane on the board
FACE = YP + DEPTH / 2 + 0.11                  # panel front face (y)
sq, sqC = prism('sq', SQ, DEPTH, M_SQ)
urt, urtC = prism('urt', URT, DEPTH, M_TRI)
llt, lltC = prism('llt', LLT, DEPTH, M_TRI)
PL = {'sq': sqC, 'urt': urtC, 'llt': lltC}
OBJ = {'sq': sq, 'urt': urt, 'llt': llt}
# fingers close across each part at its centroid; half-width of the part there
HW = {'sq': 0.33, 'urt': 0.393, 'llt': 0.39}
