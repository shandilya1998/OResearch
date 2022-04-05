from libc.stdio cimport FILE

cdef extern from "gurobi_c.h":

    ctypedef struct GRBmodel:
        pass

    ctypedef struct GRBenv:
        pass
    #/* Version numbers */

    int GRB_VERSION_MAJOR=     8
    int GRB_VERSION_MINOR=     0
    int GRB_VERSION_TECHNICAL= 1

    #/* Default and max priority for Compute Server jobs */

    int DEFAULT_CS_PRIORITY= 0
    int MAX_CS_PRIORITY= 100

    #/* Default port number for Compute Server */

    int DEFAULT_CS_PORT= 61000

    #/* Default Compute Server hangup duration */

    int DEFAULT_CS_HANGUP= 60

    #/* Error codes */

    int GRB_ERROR_OUT_OF_MEMORY=            10001
    int GRB_ERROR_NULL_ARGUMENT=            10002
    int GRB_ERROR_INVALID_ARGUMENT=         10003
    int GRB_ERROR_UNKNOWN_ATTRIBUTE=        10004
    int GRB_ERROR_DATA_NOT_AVAILABLE=       10005
    int GRB_ERROR_INDEX_OUT_OF_RANGE=       10006
    int GRB_ERROR_UNKNOWN_PARAMETER=        10007
    int GRB_ERROR_VALUE_OUT_OF_RANGE=       10008
    int GRB_ERROR_NO_LICENSE=               10009
    int GRB_ERROR_SIZE_LIMIT_EXCEEDED=      10010
    int GRB_ERROR_CALLBACK=                 10011
    int GRB_ERROR_FILE_READ=                10012
    int GRB_ERROR_FILE_WRITE=               10013
    int GRB_ERROR_NUMERIC=                  10014
    int GRB_ERROR_IIS_NOT_INFEASIBLE=       10015
    int GRB_ERROR_NOT_FOR_MIP=              10016
    int GRB_ERROR_OPTIMIZATION_IN_PROGRESS= 10017
    int GRB_ERROR_DUPLICATES=               10018
    int GRB_ERROR_NODEFILE=                 10019
    int GRB_ERROR_Q_NOT_PSD=                10020
    int GRB_ERROR_QCP_EQUALITY_CONSTRAINT=  10021
    int GRB_ERROR_NETWORK=                  10022
    int GRB_ERROR_JOB_REJECTED=             10023
    int GRB_ERROR_NOT_SUPPORTED=            10024
    int GRB_ERROR_EXCEED_2B_NONZEROS=       10025
    int GRB_ERROR_INVALID_PIECEWISE_OBJ=    10026
    int GRB_ERROR_UPDATEMODE_CHANGE=        10027
    int GRB_ERROR_CLOUD=                    10028
    int GRB_ERROR_MODEL_MODIFICATION=       10029
    int GRB_ERROR_CSWORKER=                 10030
    int GRB_ERROR_TUNE_MODEL_TYPES=         10031

    #/* Constraint senses */

    char GRB_LESS_EQUAL=    '<'
    char GRB_GREATER_EQUAL= '>'
    char GRB_EQUAL=         '='

    #/* Variable types */

    char GRB_CONTINUOUS= 'C'
    char GRB_BINARY=     'B'
    char GRB_INTEGER=    'I'
    char GRB_SEMICONT=   'S'
    char GRB_SEMIINT=    'N'

    #/* Objective sense */

    int GRB_MINIMIZE= 1
    int GRB_MAXIMIZE= -1

    #/* SOS types */

    int GRB_SOS_TYPE1= 1
    int GRB_SOS_TYPE2= 2

    #/* Numeric constants */

    float GRB_INFINITY=  1e100
    float GRB_UNDEFINED= 1e101
    int GRB_MAXINT=    2000000000

    #/* Limits */

    int GRB_MAX_NAMELEN=    255
    int GRB_MAX_STRLEN=     512
    int GRB_MAX_CONCURRENT= 64
    
    char* GRB_INT_ATTR_NUMCONSTRS=    "NumConstrs"    #/* # of constraints */
    char* GRB_INT_ATTR_NUMVARS=       "NumVars"       #/* # of vars */
    char* GRB_INT_ATTR_NUMSOS=        "NumSOS"        #/* # of sos constraints */
    char* GRB_INT_ATTR_NUMQCONSTRS=   "NumQConstrs"   #/* # of quadratic constraints */
    char* GRB_INT_ATTR_NUMGENCONSTRS= "NumGenConstrs" #/* # of general constraints */
    char* GRB_INT_ATTR_NUMNZS=        "NumNZs"        #/* # of nz in A */
    char* GRB_DBL_ATTR_DNUMNZS=       "DNumNZs"       #/* # of nz in A */
    char* GRB_INT_ATTR_NUMQNZS=       "NumQNZs"       #/* # of nz in Q */
    char* GRB_INT_ATTR_NUMQCNZS=      "NumQCNZs"      #/* # of nz in q constraints */
    char* GRB_INT_ATTR_NUMINTVARS=    "NumIntVars"    #/* # of integer vars */
    char* GRB_INT_ATTR_NUMBINVARS=    "NumBinVars"    #/* # of binary vars */
    char* GRB_INT_ATTR_NUMPWLOBJVARS= "NumPWLObjVars" #/* # of variables with PWL obj. */
    char* GRB_STR_ATTR_MODELNAME=     "ModelName"     #/* model name */
    char* GRB_INT_ATTR_MODELSENSE=    "ModelSense"    #/* 1=min, -1=max */
    char* GRB_DBL_ATTR_OBJCON=        "ObjCon"        #/* Objective constant */
    char* GRB_INT_ATTR_IS_MIP=        "IsMIP"         #/* Is model a MIP? */
    char* GRB_INT_ATTR_IS_QP=         "IsQP"          #/* Model has quadratic obj? */
    char* GRB_INT_ATTR_IS_QCP=        "IsQCP"         #/* Model has quadratic constr? */
    char* GRB_INT_ATTR_IS_MULTIOBJ=   "IsMultiObj"    #/* Model has multiple objectives? */
    char* GRB_STR_ATTR_SERVER=        "Server"        #/* Name of Compute Server */
    char* GRB_STR_ATTR_JOBID=         "JobID"         #/* Compute Server job ID */
    char* GRB_INT_ATTR_LICENSE_EXPIRATION= "LicenseExpiration" #/* License expiration date */

    #/* Variable attributes */

    char* GRB_DBL_ATTR_LB=             "LB"              #/* Lower bound */
    char* GRB_DBL_ATTR_UB=             "UB"              #/* Upper bound */
    char* GRB_DBL_ATTR_OBJ=            "Obj"             #/* Objective coeff */
    char* GRB_CHAR_ATTR_VTYPE=         "VType"           #/* Integrality type */
    char* GRB_DBL_ATTR_START=          "Start"           #/* MIP start value */
    char* GRB_DBL_ATTR_PSTART=         "PStart"          #/* LP primal solution warm start */
    char* GRB_INT_ATTR_BRANCHPRIORITY= "BranchPriority"  #/* MIP branch priority */
    char* GRB_STR_ATTR_VARNAME=        "VarName"         #/* Variable name */
    char* GRB_INT_ATTR_PWLOBJCVX=      "PWLObjCvx"       #/* Convexity of variable PWL obj */
    char* GRB_DBL_ATTR_VARHINTVAL=     "VarHintVal"
    char* GRB_INT_ATTR_VARHINTPRI=     "VarHintPri"
    char* GRB_INT_ATTR_PARTITION=      "Partition"

    #/* Constraint attributes */

    char* GRB_DBL_ATTR_RHS=        "RHS"        #/* RHS */
    char* GRB_DBL_ATTR_DSTART=     "DStart"     #/* LP dual solution warm start */
    char* GRB_CHAR_ATTR_SENSE=     "Sense"      #/* Sense ('<', '>', or '=') */
    char* GRB_STR_ATTR_CONSTRNAME= "ConstrName" #/* Constraint name */
    char* GRB_INT_ATTR_LAZY=       "Lazy"       #/* Lazy constraint? */

    #/* Quadratic constraint attributes */

    char* GRB_DBL_ATTR_QCRHS=    "QCRHS"   #/* QC RHS */
    char* GRB_CHAR_ATTR_QCSENSE= "QCSense" #/* QC sense ('<', '>', or '=') */
    char* GRB_STR_ATTR_QCNAME=   "QCName"  #/* QC name */

    #/* General constraint attributes */

    char* GRB_INT_ATTR_GENCONSTRTYPE=  "GenConstrType"  #/* Type of general constraint */
    char* GRB_STR_ATTR_GENCONSTRNAME=  "GenConstrName"  #/* Name of general constraint */

    #/* Model statistics */

    char* GRB_DBL_ATTR_MAX_COEFF=      "MaxCoeff"     #/* Max (abs) nz coeff in A */
    char* GRB_DBL_ATTR_MIN_COEFF=      "MinCoeff"     #/* Min (abs) nz coeff in A */
    char* GRB_DBL_ATTR_MAX_BOUND=      "MaxBound"     #/* Max (abs) finite var bd */
    char* GRB_DBL_ATTR_MIN_BOUND=      "MinBound"     #/* Min (abs) var bd */
    char* GRB_DBL_ATTR_MAX_OBJ_COEFF=  "MaxObjCoeff"  #/* Max (abs) obj coeff */
    char* GRB_DBL_ATTR_MIN_OBJ_COEFF=  "MinObjCoeff"  #/* Min (abs) obj coeff */
    char* GRB_DBL_ATTR_MAX_RHS=        "MaxRHS"       #/* Max (abs) rhs coeff */
    char* GRB_DBL_ATTR_MIN_RHS=        "MinRHS"       #/* Min (abs) rhs coeff */
    char* GRB_DBL_ATTR_MAX_QCCOEFF=    "MaxQCCoeff"   #/* Max (abs) nz coeff in Q */
    char* GRB_DBL_ATTR_MIN_QCCOEFF=    "MinQCCoeff"   #/* Min (abs) nz coeff in Q */
    char* GRB_DBL_ATTR_MAX_QOBJ_COEFF= "MaxQObjCoeff" #/* Max (abs) obj coeff of quadratic part */
    char* GRB_DBL_ATTR_MIN_QOBJ_COEFF= "MinQObjCoeff" #/* Min (abs) obj coeff of quadratic part */
    char* GRB_DBL_ATTR_MAX_QCLCOEFF=   "MaxQCLCoeff"  #/* Max (abs) nz coeff in linear part of Q */
    char* GRB_DBL_ATTR_MIN_QCLCOEFF=   "MinQCLCoeff"  #/* Min (abs) nz coeff in linear part of Q */
    char* GRB_DBL_ATTR_MAX_QCRHS=      "MaxQCRHS"     #/* Max (abs) rhs of Q */
    char* GRB_DBL_ATTR_MIN_QCRHS=      "MinQCRHS"     #/* Min (abs) rhs of Q */

    #/* Model solution attributes */

    char* GRB_DBL_ATTR_RUNTIME=       "Runtime"     #/* Run time for optimization */
    char* GRB_INT_ATTR_STATUS=        "Status"      #/* Optimization status */
    char* GRB_DBL_ATTR_OBJVAL=        "ObjVal"      #/* Solution objective */
    char* GRB_DBL_ATTR_OBJBOUND=      "ObjBound"    #/* Best bound on solution */
    char* GRB_DBL_ATTR_OBJBOUNDC=     "ObjBoundC"   #/* Continuous bound */
    char* GRB_DBL_ATTR_POOLOBJBOUND=  "PoolObjBound" #/* Best bound on pool solution */
    char* GRB_DBL_ATTR_POOLOBJVAL=    "PoolObjVal"  #/* Solution objective for solutionnumber */
    char* GRB_DBL_ATTR_MIPGAP=        "MIPGap"      #/* MIP optimality gap */
    char* GRB_INT_ATTR_SOLCOUNT=      "SolCount"    #/* # of solutions found */
    char* GRB_DBL_ATTR_ITERCOUNT=     "IterCount"   #/* Iters performed (simplex) */
    char* GRB_INT_ATTR_BARITERCOUNT=  "BarIterCount" #/* Iters performed (barrier) */
    char* GRB_DBL_ATTR_NODECOUNT=     "NodeCount"    #/* Nodes explored (B&C) */
    char* GRB_DBL_ATTR_OPENNODECOUNT= "OpenNodeCount" #/* Unexplored nodes (B&C) */
    char* GRB_INT_ATTR_HASDUALNORM=   "HasDualNorm"  #/* 0, no basis,
                                                   #      1, has basis, so can be computed
                                                   #      2, available */

    #/* Variable attributes related to the current solution */

    char* GRB_DBL_ATTR_X=         "X"         #/* Solution value */
    char* GRB_DBL_ATTR_XN=        "Xn"        #/* Alternate MIP solution */
    char* GRB_DBL_ATTR_BARX=      "BarX"      #/* Best barrier iterate */
    char* GRB_DBL_ATTR_RC=        "RC"        #/* Reduced costs */
    char* GRB_DBL_ATTR_VDUALNORM= "VDualNorm" #/* Dual norm square */
    char* GRB_INT_ATTR_VBASIS=    "VBasis"    #/* Variable basis status */

    #/* Constraint attributes related to the current solution */

    char* GRB_DBL_ATTR_PI=        "Pi"        #/* Dual value */
    char* GRB_DBL_ATTR_QCPI=      "QCPi"      #/* Dual value for QC */
    char* GRB_DBL_ATTR_SLACK=     "Slack"     #/* Constraint slack */
    char* GRB_DBL_ATTR_QCSLACK=   "QCSlack"   #/* QC Constraint slack */
    char* GRB_DBL_ATTR_CDUALNORM= "CDualNorm" #/* Dual norm square */
    char* GRB_INT_ATTR_CBASIS=    "CBasis"    #/* Constraint basis status */

    #/* Solution quality attributes */

    char* GRB_DBL_ATTR_BOUND_VIO=              "BoundVio"
    char* GRB_DBL_ATTR_BOUND_SVIO=             "BoundSVio"
    char* GRB_INT_ATTR_BOUND_VIO_INDEX=        "BoundVioIndex"
    char* GRB_INT_ATTR_BOUND_SVIO_INDEX=       "BoundSVioIndex"
    char* GRB_DBL_ATTR_BOUND_VIO_SUM=          "BoundVioSum"
    char* GRB_DBL_ATTR_BOUND_SVIO_SUM=         "BoundSVioSum"
    char* GRB_DBL_ATTR_CONSTR_VIO=             "ConstrVio"
    char* GRB_DBL_ATTR_CONSTR_SVIO=            "ConstrSVio"
    char* GRB_INT_ATTR_CONSTR_VIO_INDEX=       "ConstrVioIndex"
    char* GRB_INT_ATTR_CONSTR_SVIO_INDEX=      "ConstrSVioIndex"
    char* GRB_DBL_ATTR_CONSTR_VIO_SUM=         "ConstrVioSum"
    char* GRB_DBL_ATTR_CONSTR_SVIO_SUM=        "ConstrSVioSum"
    char* GRB_DBL_ATTR_CONSTR_RESIDUAL=        "ConstrResidual"
    char* GRB_DBL_ATTR_CONSTR_SRESIDUAL=       "ConstrSResidual"
    char* GRB_INT_ATTR_CONSTR_RESIDUAL_INDEX=  "ConstrResidualIndex"
    char* GRB_INT_ATTR_CONSTR_SRESIDUAL_INDEX= "ConstrSResidualIndex"
    char* GRB_DBL_ATTR_CONSTR_RESIDUAL_SUM=    "ConstrResidualSum"
    char* GRB_DBL_ATTR_CONSTR_SRESIDUAL_SUM=   "ConstrSResidualSum"
    char* GRB_DBL_ATTR_DUAL_VIO=               "DualVio"
    char* GRB_DBL_ATTR_DUAL_SVIO=              "DualSVio"
    char* GRB_INT_ATTR_DUAL_VIO_INDEX=         "DualVioIndex"
    char* GRB_INT_ATTR_DUAL_SVIO_INDEX=        "DualSVioIndex"
    char* GRB_DBL_ATTR_DUAL_VIO_SUM=           "DualVioSum"
    char* GRB_DBL_ATTR_DUAL_SVIO_SUM=          "DualSVioSum"
    char* GRB_DBL_ATTR_DUAL_RESIDUAL=          "DualResidual"
    char* GRB_DBL_ATTR_DUAL_SRESIDUAL=         "DualSResidual"
    char* GRB_INT_ATTR_DUAL_RESIDUAL_INDEX=    "DualResidualIndex"
    char* GRB_INT_ATTR_DUAL_SRESIDUAL_INDEX=   "DualSResidualIndex"
    char* GRB_DBL_ATTR_DUAL_RESIDUAL_SUM=      "DualResidualSum"
    char* GRB_DBL_ATTR_DUAL_SRESIDUAL_SUM=     "DualSResidualSum"
    char* GRB_DBL_ATTR_INT_VIO=                "IntVio"
    char* GRB_INT_ATTR_INT_VIO_INDEX=          "IntVioIndex"
    char* GRB_DBL_ATTR_INT_VIO_SUM=            "IntVioSum"
    char* GRB_DBL_ATTR_COMPL_VIO=              "ComplVio"
    char* GRB_INT_ATTR_COMPL_VIO_INDEX=        "ComplVioIndex"
    char* GRB_DBL_ATTR_COMPL_VIO_SUM=          "ComplVioSum"
    char* GRB_DBL_ATTR_KAPPA=                  "Kappa"
    char* GRB_DBL_ATTR_KAPPA_EXACT=            "KappaExact"
    char* GRB_DBL_ATTR_N2KAPPA=                "N2Kappa"

    #/* LP sensitivity analysis */

    char* GRB_DBL_ATTR_SA_OBJLOW= "SAObjLow"
    char* GRB_DBL_ATTR_SA_OBJUP=  "SAObjUp"
    char* GRB_DBL_ATTR_SA_LBLOW=  "SALBLow"
    char* GRB_DBL_ATTR_SA_LBUP=   "SALBUp"
    char* GRB_DBL_ATTR_SA_UBLOW=  "SAUBLow"
    char* GRB_DBL_ATTR_SA_UBUP=   "SAUBUp"
    char* GRB_DBL_ATTR_SA_RHSLOW= "SARHSLow"
    char* GRB_DBL_ATTR_SA_RHSUP=  "SARHSUp"

    #/* IIS */

    char* GRB_INT_ATTR_IIS_MINIMAL=   "IISMinimal"   #/* Boolean: Is IIS Minimal? */
    char* GRB_INT_ATTR_IIS_LB=        "IISLB"        #/* Boolean: Is var LB in IIS? */
    char* GRB_INT_ATTR_IIS_UB=        "IISUB"        #/* Boolean: Is var UB in IIS? */
    char* GRB_INT_ATTR_IIS_CONSTR=    "IISConstr"    #/* Boolean: Is constr in IIS? */
    char* GRB_INT_ATTR_IIS_SOS=       "IISSOS"       #/* Boolean: Is SOS in IIS? */
    char* GRB_INT_ATTR_IIS_QCONSTR=   "IISQConstr"   #/* Boolean: Is QConstr in IIS? */
    char* GRB_INT_ATTR_IIS_GENCONSTR= "IISGenConstr" #/* Boolean: Is general constr in IIS? */

    #/* Tuning */

    char* GRB_INT_ATTR_TUNE_RESULTCOUNT "TuneResultCount"

    #/* Advanced simplex features */

    char* GRB_DBL_ATTR_FARKASDUAL=  "FarkasDual"
    char* GRB_DBL_ATTR_FARKASPROOF= "FarkasProof"
    char* GRB_DBL_ATTR_UNBDRAY=     "UnbdRay"
    char* GRB_INT_ATTR_INFEASVAR=   "InfeasVar"
    char* GRB_INT_ATTR_UNBDVAR=     "UnbdVar"

    #/* Presolve attribute */

    char* GRB_INT_ATTR_VARPRESTAT= "VarPreStat"
    char* GRB_DBL_ATTR_PREFIXVAL=  "PreFixVal"

    #/* Multi objective attribute, controlled by parameter ObjNumber (= i) */

    char* GRB_DBL_ATTR_OBJN=         "ObjN"         #/* ith objective */
    char* GRB_DBL_ATTR_OBJNVAL=      "ObjNVal"      #/* Solution objective for Multi-objectives */
    char* GRB_DBL_ATTR_OBJNCON=      "ObjNCon"      #/* constant term */
    char* GRB_DBL_ATTR_OBJNWEIGHT=   "ObjNWeight"   #/* weight */
    char* GRB_INT_ATTR_OBJNPRIORITY= "ObjNPriority" #/* priority */
    char* GRB_DBL_ATTR_OBJNRELTOL=   "ObjNRelTol"   #/* relative tolerance */
    char* GRB_DBL_ATTR_OBJNABSTOL=   "ObjNAbsTol"   #/* absolute tolerance */
    char* GRB_STR_ATTR_OBJNNAME=     "ObjNName"     #/* name */
    char* GRB_INT_ATTR_NUMOBJ=       "NumObj"       #/* number of objectives */
    char* GRB_INT_ATTR_NUMSTART=     "NumStart"     #/* number of MIP starts */

    #/* Alternate define */
    char* GRB_DBL_ATTR_Xn= "Xn"
    
    #/* General constraints */

    int GRB_GENCONSTR_MAX=         0
    int GRB_GENCONSTR_MIN=         1
    int GRB_GENCONSTR_ABS=         2
    int GRB_GENCONSTR_AND=         3
    int GRB_GENCONSTR_OR=          4
    int GRB_GENCONSTR_INDICATOR=   5


    #/*
    #   CALLBACKS
    #*/

    #/* For callback */

    int GRB_CB_POLLING=   0
    int GRB_CB_PRESOLVE=  1
    int GRB_CB_SIMPLEX=   2
    int GRB_CB_MIP=       3
    int GRB_CB_MIPSOL=    4
    int GRB_CB_MIPNODE=   5
    int GRB_CB_MESSAGE=   6
    int GRB_CB_BARRIER=   7
    int GRB_CB_MULTIOBJ=  8

    #/* Supported names for callback */

    int GRB_CB_PRE_COLDEL=  1000
    int GRB_CB_PRE_ROWDEL=  1001
    int GRB_CB_PRE_SENCHG=  1002
    int GRB_CB_PRE_BNDCHG=  1003
    int GRB_CB_PRE_COECHG=  1004

    int GRB_CB_SPX_ITRCNT=  2000
    int GRB_CB_SPX_OBJVAL=  2001
    int GRB_CB_SPX_PRIMINF= 2002
    int GRB_CB_SPX_DUALINF= 2003
    int GRB_CB_SPX_ISPERT=  2004

    int GRB_CB_MIP_OBJBST=  3000
    int GRB_CB_MIP_OBJBND=  3001
    int GRB_CB_MIP_NODCNT=  3002
    int GRB_CB_MIP_SOLCNT=  3003
    int GRB_CB_MIP_CUTCNT=  3004
    int GRB_CB_MIP_NODLFT=  3005
    int GRB_CB_MIP_ITRCNT=  3006
    int GRB_CB_MIP_OBJBNDC= 3007

    int GRB_CB_MIPSOL_SOL=     4001
    int GRB_CB_MIPSOL_OBJ=     4002
    int GRB_CB_MIPSOL_OBJBST=  4003
    int GRB_CB_MIPSOL_OBJBND=  4004
    int GRB_CB_MIPSOL_NODCNT=  4005
    int GRB_CB_MIPSOL_SOLCNT=  4006
    int GRB_CB_MIPSOL_OBJBNDC= 4007

    int GRB_CB_MIPNODE_STATUS=  5001
    int GRB_CB_MIPNODE_REL=     5002
    int GRB_CB_MIPNODE_OBJBST=  5003
    int GRB_CB_MIPNODE_OBJBND=  5004
    int GRB_CB_MIPNODE_NODCNT=  5005
    int GRB_CB_MIPNODE_SOLCNT=  5006
    int GRB_CB_MIPNODE_BRVAR=   5007
    int GRB_CB_MIPNODE_OBJBNDC= 5008

    int GRB_CB_MSG_STRING=  6001
    int GRB_CB_RUNTIME=     6002

    int GRB_CB_BARRIER_ITRCNT=  7001
    int GRB_CB_BARRIER_PRIMOBJ= 7002
    int GRB_CB_BARRIER_DUALOBJ= 7003
    int GRB_CB_BARRIER_PRIMINF= 7004
    int GRB_CB_BARRIER_DUALINF= 7005
    int GRB_CB_BARRIER_COMPL=   7006

    int GRB_CB_MULTIOBJ_OBJCNT=  8001
    int GRB_CB_MULTIOBJ_SOLCNT=  8002
    int GRB_CB_MULTIOBJ_SOL=     8003

    int GRB_FEASRELAX_LINEAR=      0
    int GRB_FEASRELAX_QUADRATIC=   1
    int GRB_FEASRELAX_CARDINALITY= 2
    
    #/* Model status codes (after call to GRBoptimize()) */

    int GRB_LOADED=          1
    int GRB_OPTIMAL=         2
    int GRB_INFEASIBLE=      3
    int GRB_INF_OR_UNBD=     4
    int GRB_UNBOUNDED=       5
    int GRB_CUTOFF=          6
    int GRB_ITERATION_LIMIT= 7
    int GRB_NODE_LIMIT=      8
    int GRB_TIME_LIMIT=      9
    int GRB_SOLUTION_LIMIT= 10
    int GRB_INTERRUPTED=    11
    int GRB_NUMERIC=        12
    int GRB_SUBOPTIMAL=     13
    int GRB_INPROGRESS=     14
    int GRB_USER_OBJ_LIMIT= 15

    #/* Basis status info */

    int GRB_BASIC=           0
    int GRB_NONBASIC_LOWER= -1
    int GRB_NONBASIC_UPPER= -2
    int GRB_SUPERBASIC=     -3
    
    #/* Termination */

    char* GRB_INT_PAR_BARITERLIMIT=   "BarIterLimit"
    char* GRB_DBL_PAR_CUTOFF=         "Cutoff"
    char* GRB_DBL_PAR_ITERATIONLIMIT= "IterationLimit"
    char* GRB_DBL_PAR_NODELIMIT=      "NodeLimit"
    char* GRB_INT_PAR_SOLUTIONLIMIT=  "SolutionLimit"
    char* GRB_DBL_PAR_TIMELIMIT=      "TimeLimit"
    char* GRB_DBL_PAR_BESTOBJSTOP=    "BestObjStop"
    char* GRB_DBL_PAR_BESTBDSTOP=     "BestBdStop"

    #/* Tolerances */

    char* GRB_DBL_PAR_FEASIBILITYTOL= "FeasibilityTol"
    char* GRB_DBL_PAR_INTFEASTOL=     "IntFeasTol"
    char* GRB_DBL_PAR_MARKOWITZTOL=   "MarkowitzTol"
    char* GRB_DBL_PAR_MIPGAP=         "MIPGap"
    char* GRB_DBL_PAR_MIPGAPABS=      "MIPGapAbs"
    char* GRB_DBL_PAR_OPTIMALITYTOL=  "OptimalityTol"
    char* GRB_DBL_PAR_PSDTOL=         "PSDTol"

    #/* Simplex */

    char* GRB_INT_PAR_METHOD=         "Method"
    char* GRB_DBL_PAR_PERTURBVALUE=   "PerturbValue"
    char* GRB_DBL_PAR_OBJSCALE=       "ObjScale"
    char* GRB_INT_PAR_SCALEFLAG=      "ScaleFlag"
    char* GRB_INT_PAR_SIMPLEXPRICING= "SimplexPricing"
    char* GRB_INT_PAR_QUAD=           "Quad"
    char* GRB_INT_PAR_NORMADJUST=     "NormAdjust"
    char* GRB_INT_PAR_SIFTING=        "Sifting"
    char* GRB_INT_PAR_SIFTMETHOD=     "SiftMethod"

    #/* Barrier */

    char* GRB_DBL_PAR_BARCONVTOL=     "BarConvTol"
    char* GRB_INT_PAR_BARCORRECTORS=  "BarCorrectors"
    char* GRB_INT_PAR_BARHOMOGENEOUS= "BarHomogeneous"
    char* GRB_INT_PAR_BARORDER=       "BarOrder"
    char* GRB_DBL_PAR_BARQCPCONVTOL=  "BarQCPConvTol"
    char* GRB_INT_PAR_CROSSOVER=      "Crossover"
    char* GRB_INT_PAR_CROSSOVERBASIS= "CrossoverBasis"

    #/* MIP */

    char* GRB_INT_PAR_BRANCHDIR=         "BranchDir"
    char* GRB_INT_PAR_DEGENMOVES=        "DegenMoves"
    char* GRB_INT_PAR_DISCONNECTED=      "Disconnected"
    char* GRB_DBL_PAR_HEURISTICS=        "Heuristics"
    char* GRB_DBL_PAR_IMPROVESTARTGAP=   "ImproveStartGap"
    char* GRB_DBL_PAR_IMPROVESTARTTIME=  "ImproveStartTime"
    char* GRB_DBL_PAR_IMPROVESTARTNODES= "ImproveStartNodes"
    char* GRB_INT_PAR_MINRELNODES=       "MinRelNodes"
    char* GRB_INT_PAR_MIPFOCUS=          "MIPFocus"
    char* GRB_STR_PAR_NODEFILEDIR=       "NodefileDir"
    char* GRB_DBL_PAR_NODEFILESTART=     "NodefileStart"
    char* GRB_INT_PAR_NODEMETHOD=        "NodeMethod"
    char* GRB_INT_PAR_NORELHEURISTIC=    "NoRelHeuristic"
    char* GRB_INT_PAR_PUMPPASSES=        "PumpPasses"
    char* GRB_INT_PAR_RINS=              "RINS"
    char* GRB_INT_PAR_STARTNODELIMIT=    "StartNodeLimit"
    char* GRB_INT_PAR_SUBMIPNODES=       "SubMIPNodes"
    char* GRB_INT_PAR_SYMMETRY=          "Symmetry"
    char* GRB_INT_PAR_VARBRANCH=         "VarBranch"
    char* GRB_INT_PAR_SOLUTIONNUMBER=    "SolutionNumber"
    char* GRB_INT_PAR_ZEROOBJNODES=      "ZeroObjNodes"

    #/* MIP cuts */

    char* GRB_INT_PAR_CUTS=            "Cuts"

    char* GRB_INT_PAR_CLIQUECUTS=      "CliqueCuts"
    char* GRB_INT_PAR_COVERCUTS=       "CoverCuts"
    char* GRB_INT_PAR_FLOWCOVERCUTS=   "FlowCoverCuts"
    char* GRB_INT_PAR_FLOWPATHCUTS=    "FlowPathCuts"
    char* GRB_INT_PAR_GUBCOVERCUTS=    "GUBCoverCuts"
    char* GRB_INT_PAR_IMPLIEDCUTS=     "ImpliedCuts"
    char* GRB_INT_PAR_PROJIMPLIEDCUTS= "ProjImpliedCuts"
    char* GRB_INT_PAR_MIPSEPCUTS=      "MIPSepCuts"
    char* GRB_INT_PAR_MIRCUTS=         "MIRCuts"
    char* GRB_INT_PAR_STRONGCGCUTS=    "StrongCGCuts"
    char* GRB_INT_PAR_MODKCUTS=        "ModKCuts"
    char* GRB_INT_PAR_ZEROHALFCUTS=    "ZeroHalfCuts"
    char* GRB_INT_PAR_NETWORKCUTS=     "NetworkCuts"
    char* GRB_INT_PAR_SUBMIPCUTS=      "SubMIPCuts"
    char* GRB_INT_PAR_INFPROOFCUTS=    "InfProofCuts"

    char* GRB_INT_PAR_CUTAGGPASSES=    "CutAggPasses"
    char* GRB_INT_PAR_CUTPASSES=       "CutPasses"
    char* GRB_INT_PAR_GOMORYPASSES=    "GomoryPasses"

    #/* Distributed algorithms */

    char* GRB_STR_PAR_WORKERPOOL=      "WorkerPool"
    char* GRB_STR_PAR_WORKERPASSWORD=  "WorkerPassword"

    #/* Other */

    char* GRB_INT_PAR_AGGREGATE=         "Aggregate"
    char* GRB_INT_PAR_AGGFILL=           "AggFill"
    char* GRB_INT_PAR_CONCURRENTMIP=     "ConcurrentMIP"
    char* GRB_INT_PAR_CONCURRENTJOBS=    "ConcurrentJobs"
    char* GRB_INT_PAR_DISPLAYINTERVAL=   "DisplayInterval"
    char* GRB_INT_PAR_DISTRIBUTEDMIPJOBS="DistributedMIPJobs"
    char* GRB_INT_PAR_DUALREDUCTIONS=    "DualReductions"
    char* GRB_DBL_PAR_FEASRELAXBIGM=     "FeasRelaxBigM"
    char* GRB_INT_PAR_IISMETHOD=         "IISMethod"
    char* GRB_INT_PAR_INFUNBDINFO=       "InfUnbdInfo"
    char* GRB_INT_PAR_LAZYCONSTRAINTS=   "LazyConstraints"
    char* GRB_STR_PAR_LOGFILE=           "LogFile"
    char* GRB_INT_PAR_LOGTOCONSOLE=      "LogToConsole"
    char* GRB_INT_PAR_MIQCPMETHOD=       "MIQCPMethod"
    char* GRB_INT_PAR_NUMERICFOCUS=      "NumericFocus"
    char* GRB_INT_PAR_OUTPUTFLAG=        "OutputFlag"
    char* GRB_INT_PAR_PRECRUSH=          "PreCrush"
    char* GRB_INT_PAR_PREDEPROW=         "PreDepRow"
    char* GRB_INT_PAR_PREDUAL=           "PreDual"
    char* GRB_INT_PAR_PREPASSES=         "PrePasses"
    char* GRB_INT_PAR_PREQLINEARIZE=     "PreQLinearize"
    char* GRB_INT_PAR_PRESOLVE=          "Presolve"
    char* GRB_DBL_PAR_PRESOS1BIGM=       "PreSOS1BigM"
    char* GRB_DBL_PAR_PRESOS2BIGM=       "PreSOS2BigM"
    char* GRB_INT_PAR_PRESPARSIFY=       "PreSparsify"
    char* GRB_INT_PAR_PREMIQCPFORM=      "PreMIQCPForm"
    char* GRB_INT_PAR_QCPDUAL=           "QCPDual"
    char* GRB_INT_PAR_RECORD=            "Record"
    char* GRB_STR_PAR_RESULTFILE=        "ResultFile"
    char* GRB_INT_PAR_SEED=              "Seed"
    char* GRB_INT_PAR_THREADS=           "Threads"
    char* GRB_DBL_PAR_TUNETIMELIMIT=     "TuneTimeLimit"
    char* GRB_INT_PAR_TUNERESULTS=       "TuneResults"
    char* GRB_INT_PAR_TUNECRITERION=     "TuneCriterion"
    char* GRB_INT_PAR_TUNETRIALS=        "TuneTrials"
    char* GRB_INT_PAR_TUNEOUTPUT=        "TuneOutput"
    char* GRB_INT_PAR_TUNEJOBS=          "TuneJobs"
    char* GRB_INT_PAR_UPDATEMODE=        "UpdateMode"
    char* GRB_INT_PAR_OBJNUMBER=         "ObjNumber"
    char* GRB_INT_PAR_MULTIOBJMETHOD=    "MultiObjMethod"
    char* GRB_INT_PAR_MULTIOBJPRE=       "MultiObjPre"
    char* GRB_INT_PAR_POOLSOLUTIONS=     "PoolSolutions"
    char* GRB_DBL_PAR_POOLGAP=           "PoolGap"
    char* GRB_INT_PAR_POOLSEARCHMODE=    "PoolSearchMode"
    char* GRB_INT_PAR_IGNORENAMES=       "IgnoreNames"
    char* GRB_INT_PAR_STARTNUMBER=       "StartNumber"
    char* GRB_INT_PAR_PARTITIONPLACE=    "PartitionPlace"
    char* GRB_STR_PAR_COMPUTESERVER=     "ComputeServer"
    char* GRB_STR_PAR_TOKENSERVER=       "TokenServer"
    char* GRB_STR_PAR_SERVERPASSWORD=    "ServerPassword"
    char* GRB_INT_PAR_SERVERTIMEOUT=     "ServerTimeout"
    char* GRB_STR_PAR_CSROUTER=          "CSRouter"
    char* GRB_INT_PAR_CSPRIORITY=        "CSPriority"
    char* GRB_INT_PAR_CSIDLETIMEOUT=     "CSIdleTimeout"
    char* GRB_INT_PAR_CSTLSINSECURE=     "TLSInsecure"
    char* GRB_INT_PAR_TSPORT=            "TSPort"
    char* GRB_STR_PAR_CLOUDACCESSID=     "CloudAccessID"
    char* GRB_STR_PAR_CLOUDSECRETKEY=    "CloudSecretKey"
    char* GRB_STR_PAR_CLOUDPOOL=         "CloudPool"
    char* GRB_STR_PAR_CLOUDHOST=         "CloudHost"
    char* GRB_STR_PAR_DUMMY=             "Dummy"

    #/* All *CUTS parameters */
    int GRB_CUTS_AUTO=          -1
    int GRB_CUTS_OFF=            0
    int GRB_CUTS_CONSERVATIVE=   1
    int GRB_CUTS_AGGRESSIVE=     2
    int GRB_CUTS_VERYAGGRESSIVE= 3

    int GRB_PRESOLVE_AUTO=        -1
    int GRB_PRESOLVE_OFF=          0
    int GRB_PRESOLVE_CONSERVATIVE= 1
    int GRB_PRESOLVE_AGGRESSIVE=   2

    int GRB_METHOD_AUTO=                            -1
    int GRB_METHOD_PRIMAL=                           0
    int GRB_METHOD_DUAL=                             1
    int GRB_METHOD_BARRIER=                          2
    int GRB_METHOD_CONCURRENT=                       3
    int GRB_METHOD_DETERMINISTIC_CONCURRENT=         4
    int GRB_METHOD_DETERMINISTIC_CONCURRENT_SIMPLEX= 5

    int GRB_BARHOMOGENEOUS_AUTO= -1
    int GRB_BARHOMOGENEOUS_OFF=   0
    int GRB_BARHOMOGENEOUS_ON=    1

    int GRB_MIPFOCUS_BALANCED=    0
    int GRB_MIPFOCUS_FEASIBILITY= 1
    int GRB_MIPFOCUS_OPTIMALITY=  2
    int GRB_MIPFOCUS_BESTBOUND=   3

    int GRB_BARORDER_AUTOMATIC=       -1
    int GRB_BARORDER_AMD=              0
    int GRB_BARORDER_NESTEDDISSECTION= 1

    int GRB_SIMPLEXPRICING_AUTO=           -1
    int GRB_SIMPLEXPRICING_PARTIAL=         0
    int GRB_SIMPLEXPRICING_STEEPEST_EDGE=   1
    int GRB_SIMPLEXPRICING_DEVEX=           2
    int GRB_SIMPLEXPRICING_STEEPEST_QUICK=  3

    int GRB_VARBRANCH_AUTO=          -1
    int GRB_VARBRANCH_PSEUDO_REDUCED= 0
    int GRB_VARBRANCH_PSEUDO_SHADOW=  1
    int GRB_VARBRANCH_MAX_INFEAS=     2
    int GRB_VARBRANCH_STRONG=         3

    int GRB_PARTITION_EARLY=     16
    int GRB_PARTITION_ROOTSTART= 8
    int GRB_PARTITION_ROOTEND=   4
    int GRB_PARTITION_NODES=     2
    int GRB_PARTITION_CLEANUP=   1

    int GRBgetattrinfo(GRBmodel* model, char* attrname, int* datatypeP, int* sizeP, int* settableP)

    int GRBisattravailable(GRBmodel* model, char* attrname)

    int GRBgetintattr(GRBmodel* model, char* attrname, int* valueP)

    int GRBsetintattr(GRBmodel* model, char* attrname, int newvalue)

    int GRBgetintattrelement(GRBmodel* model, char* attrname, int element, int* valueP)

    int GRBsetintattrelement(GRBmodel* model, char* attrname, int element, int newvalue)

    int GRBgetintattrarray(GRBmodel* model, char* attrname, int first, int len, int* values)

    int GRBsetintattrarray(GRBmodel* model, char* attrname, int first, int len, int* newvalues)

    int GRBgetintattrlist(GRBmodel* model, char* attrname, int len, int* ind, int* values)

    int GRBsetintattrlist(GRBmodel* model, char* attrname, int len, int* ind, int* newvalues)

    int GRBgetcharattrelement(GRBmodel* model, char* attrname, int element, char* valueP)

    int GRBsetcharattrelement(GRBmodel* model, char* attrname, int element, char newvalue)

    int GRBgetcharattrarray(GRBmodel* model, char* attrname, int first, int len, char* values)

    int GRBsetcharattrarray(GRBmodel* model, char* attrname, int first, int len, char* newvalues)

    int GRBgetcharattrlist(GRBmodel* model, char* attrname, int len, int* ind, char* values)

    int GRBsetcharattrlist(GRBmodel* model, char* attrname, int len, int* ind, char* newvalues)

    int GRBgetdblattr(GRBmodel* model, char* attrname, double* valueP)

    int GRBsetdblattr(GRBmodel* model, char* attrname, double newvalue)

    int GRBgetdblattrelement(GRBmodel* model, char* attrname, int element, double* valueP)

    int GRBsetdblattrelement(GRBmodel* model, char* attrname, int element, double newvalue)

    int GRBgetdblattrarray(GRBmodel* model, char* attrname, int first, int len, double* values)

    int GRBsetdblattrarray(GRBmodel* model, char* attrname, int first, int len, double* newvalues)

    int GRBgetdblattrlist(GRBmodel* model, char* attrname, int len, int* ind, double* values)

    int GRBsetdblattrlist(GRBmodel* model, char* attrname, int len, int* ind, double* newvalues)

    int GRBgetstrattr(GRBmodel* model, char* attrname, char** valueP)

    int GRBsetstrattr(GRBmodel* model, char* attrname, char* newvalue)

    int GRBgetstrattrelement(GRBmodel* model, char* attrname, int element, char** valueP)

    int GRBsetstrattrelement(GRBmodel* model, char* attrname, int element, char* newvalue)

    int GRBgetstrattrarray(GRBmodel* model, char* attrname, int first, int len, char** values)

    int GRBsetstrattrarray(GRBmodel* model, char* attrname, int first, int len, char** newvalues)

    int GRBgetstrattrlist(GRBmodel* model, char* attrname, int len, int* ind, char** values)

    int GRBsetstrattrlist(GRBmodel* model, char* attrname, int len, int* ind, char** newvalues)

    ctypedef int (*_GRBsetcallbackfunc_cb_ft)(GRBmodel* model, void* cbdata, int where, void* usrdata)

    int GRBsetcallbackfunc(GRBmodel* model, _GRBsetcallbackfunc_cb_ft cb, void* usrdata)

    ctypedef int (*_GRBgetcallbackfunc_cbP_ft)(GRBmodel* model, void* cbdata, int where, void* usrdata)

    int GRBgetcallbackfunc(GRBmodel* model, _GRBgetcallbackfunc_cbP_ft cbP)

    ctypedef int (*_GRBsetlogcallbackfunc_cb_ft)(char* msg)

    int GRBsetlogcallbackfunc(GRBmodel* model, _GRBsetlogcallbackfunc_cb_ft cb)

    ctypedef int (*_GRBsetlogcallbackfuncenv_cb_ft)(char* msg)

    int GRBsetlogcallbackfuncenv(GRBenv* env, _GRBsetlogcallbackfuncenv_cb_ft cb)

    int GRBcbget(void* cbdata, int where, int what, void* resultP)

    int GRBcbsetparam(void* cbdata, char* paramname, char* newvalue)

    int GRBcbsolution(void* cbdata, double* solution, double* objvalP)

    int GRBcbcut(void* cbdata, int cutlen, int* cutind, double* cutval, char cutsense, double cutrhs)

    int GRBcblazy(void* cbdata, int lazylen, int* lazyind, double* lazyval, char lazysense, double lazyrhs)

    int GRBgetcoeff(GRBmodel* model, int constr, int var, double* valP)

    int GRBgetconstrs(GRBmodel* model, int* numnzP, int* cbeg, int* cind, double* cval, int start, int len)

    int GRBXgetconstrs(GRBmodel* model, size_t* numnzP, size_t* cbeg, int* cind, double* cval, int start, int len)

    int GRBgetvars(GRBmodel* model, int* numnzP, int* vbeg, int* vind, double* vval, int start, int len)

    int GRBXgetvars(GRBmodel* model, size_t* numnzP, size_t* vbeg, int* vind, double* vval, int start, int len)

    int GRBgetsos(GRBmodel* model, int* nummembersP, int* sostype, int* beg, int* ind, double* weight, int start, int len)

    int GRBgetgenconstrMax(GRBmodel* model, int genconstr, int* resvarP, int* nvarsP, int* vars, double* constantP)

    int GRBgetgenconstrMin(GRBmodel* model, int genconstr, int* resvarP, int* nvarsP, int* vars, double* constantP)

    int GRBgetgenconstrAbs(GRBmodel* model, int genconstr, int* resvarP, int* argvarP)

    int GRBgetgenconstrAnd(GRBmodel* model, int genconstr, int* resvarP, int* nvarsP, int* vars)

    int GRBgetgenconstrOr(GRBmodel* model, int genconstr, int* resvarP, int* nvarsP, int* vars)

    int GRBgetgenconstrIndicator(GRBmodel* model, int genconstr, int* binvarP, int* binvalP, int* nvarsP, int* vars, double* vals, char* senseP, double* rhsP)

    int GRBgetq(GRBmodel* model, int* numqnzP, int* qrow, int* qcol, double* qval)

    int GRBgetqconstr(GRBmodel* model, int qconstr, int* numlnzP, int* lind, double* lval, int* numqnzP, int* qrow, int* qcol, double* qval)

    int GRBgetvarbyname(GRBmodel* model, char* name, int* indexP)

    int GRBgetconstrbyname(GRBmodel* model, char* name, int* indexP)

    int GRBgetpwlobj(GRBmodel* model, int var, int* pointsP, double* x, double* y)

    int GRBoptimize(GRBmodel* model)

    int GRBoptimizeasync(GRBmodel* model)

    GRBmodel* GRBcopymodel(GRBmodel* model)

    GRBmodel* GRBfixedmodel(GRBmodel* model)

    int GRBfeasrelax(GRBmodel* model, int relaxobjtype, int minrelax, double* lbpen, double* ubpen, double* rhspen, double* feasobjP)

    int GRBgetcbwhatinfo(void* cbdata, int what, int* typeP, int* sizeP)

    GRBmodel* GRBrelaxmodel(GRBmodel* model)

    int GRBconverttofixed(GRBmodel* model)

    GRBmodel* GRBpresolvemodel(GRBmodel* model)

    GRBmodel* GRBiismodel(GRBmodel* model)

    GRBmodel* GRBfeasibility(GRBmodel* model)

    GRBmodel* GRBlinearizemodel(GRBmodel* model)

    ctypedef void* (*_GRBloadenvsyscb_malloccb_ft)(size_t size, void* syscbusrdata)

    ctypedef void* (*_GRBloadenvsyscb_calloccb_ft)(size_t nmemb, size_t size, void* syscbusrdata)

    ctypedef void* (*_GRBloadenvsyscb_realloccb_ft)(void* ptr, size_t size, void* syscbusrdata)

    ctypedef void (*_GRBloadenvsyscb_freecb_ft)(void* ptr, void* syscbusrdata)

    ctypedef void (*_GRBloadenvsyscb_threadcreatecb_start_routine_ft)(void*)

    ctypedef int (*_GRBloadenvsyscb_threadcreatecb_ft)(void** threadP, _GRBloadenvsyscb_threadcreatecb_start_routine_ft start_routine, void* arg, void* syscbusrdata)

    ctypedef void (*_GRBloadenvsyscb_threadjoincb_ft)(void* thread, void* syscbusrdata)

    int GRBloadenvsyscb(GRBenv** envP, char* logfilename, _GRBloadenvsyscb_malloccb_ft malloccb, _GRBloadenvsyscb_calloccb_ft calloccb, _GRBloadenvsyscb_realloccb_ft realloccb, _GRBloadenvsyscb_freecb_ft freecb, _GRBloadenvsyscb_threadcreatecb_ft threadcreatecb, _GRBloadenvsyscb_threadjoincb_ft threadjoincb, void* syscbusrdata)

    int GRBreadmodel(GRBenv* env, char* filename, GRBmodel** modelP)

    int GRBread(GRBmodel* model, char* filename)

    int GRBwrite(GRBmodel* model, char* filename)

    int GRBismodelfile(char* filename)

    int GRBfiletype(char* filename)

    int GRBisrecordfile(char* filename)

    int GRBnewmodel(GRBenv* env, GRBmodel** modelP, char* Pname, int numvars, double* obj, double* lb, double* ub, char* vtype, char** varnames)

    int GRBloadmodel(GRBenv* env, GRBmodel** modelP, char* Pname, int numvars, int numconstrs, int objsense, double objcon, double* obj, char* sense, double* rhs, int* vbeg, int* vlen, int* vind, double* vval, double* lb, double* ub, char* vtype, char** varnames, char** constrnames)

    int GRBXloadmodel(GRBenv* env, GRBmodel** modelP, char* Pname, int numvars, int numconstrs, int objsense, double objcon, double* obj, char* sense, double* rhs, size_t* vbeg, int* vlen, int* vind, double* vval, double* lb, double* ub, char* vtype, char** varnames, char** constrnames)

    int GRBaddvar(GRBmodel* model, int numnz, int* vind, double* vval, double obj, double lb, double ub, char vtype, char* varname)

    int GRBaddvars(GRBmodel* model, int numvars, int numnz, int* vbeg, int* vind, double* vval, double* obj, double* lb, double* ub, char* vtype, char** varnames)

    int GRBXaddvars(GRBmodel* model, int numvars, size_t numnz, size_t* vbeg, int* vind, double* vval, double* obj, double* lb, double* ub, char* vtype, char** varnames)

    int GRBaddconstr(GRBmodel* model, int numnz, int* cind, double* cval, char sense, double rhs, char* constrname)

    int GRBaddconstrs(GRBmodel* model, int numconstrs, int numnz, int* cbeg, int* cind, double* cval, char* sense, double* rhs, char** constrnames)

    int GRBXaddconstrs(GRBmodel* model, int numconstrs, size_t numnz, size_t* cbeg, int* cind, double* cval, char* sense, double* rhs, char** constrnames)

    int GRBaddrangeconstr(GRBmodel* model, int numnz, int* cind, double* cval, double lower, double upper, char* constrname)

    int GRBaddrangeconstrs(GRBmodel* model, int numconstrs, int numnz, int* cbeg, int* cind, double* cval, double* lower, double* upper, char** constrnames)

    int GRBXaddrangeconstrs(GRBmodel* model, int numconstrs, size_t numnz, size_t* cbeg, int* cind, double* cval, double* lower, double* upper, char** constrnames)

    int GRBaddsos(GRBmodel* model, int numsos, int nummembers, int* types, int* beg, int* ind, double* weight)

    int GRBaddgenconstrMax(GRBmodel* model, char* name, int resvar, int nvars, int* vars, double constant)

    int GRBaddgenconstrMin(GRBmodel* model, char* name, int resvar, int nvars, int* vars, double constant)

    int GRBaddgenconstrAbs(GRBmodel* model, char* name, int resvar, int argvar)

    int GRBaddgenconstrAnd(GRBmodel* model, char* name, int resvar, int nvars, int* vars)

    int GRBaddgenconstrOr(GRBmodel* model, char* name, int resvar, int nvars, int* vars)

    int GRBaddgenconstrIndicator(GRBmodel* lp, char* name, int binvar, int binval, int nvars, int* vars, double* vals, char sense, double rhs)

    int GRBaddqconstr(GRBmodel* model, int numlnz, int* lind, double* lval, int numqnz, int* qrow, int* qcol, double* qval, char sense, double rhs, char* QCname)

    int GRBaddcone(GRBmodel* model, int nummembers, int* members)

    int GRBaddqpterms(GRBmodel* model, int numqnz, int* qrow, int* qcol, double* qval)

    int GRBdelvars(GRBmodel* model, int len, int* ind)

    int GRBdelconstrs(GRBmodel* model, int len, int* ind)

    int GRBdelsos(GRBmodel* model, int len, int* ind)

    int GRBdelgenconstrs(GRBmodel* model, int len, int* ind)

    int GRBdelqconstrs(GRBmodel* model, int len, int* ind)

    int GRBdelq(GRBmodel* model)

    int GRBchgcoeffs(GRBmodel* model, int cnt, int* cind, int* vind, double* val)

    int GRBXchgcoeffs(GRBmodel* model, size_t cnt, int* cind, int* vind, double* val)

    int GRBsetpwlobj(GRBmodel* model, int var, int points, double* x, double* y)

    int GRBupdatemodel(GRBmodel* model)

    int GRBreset(GRBmodel* model, int clearall)

    int GRBresetmodel(GRBmodel* model)

    int GRBfreemodel(GRBmodel* model)

    int GRBcomputeIIS(GRBmodel* model)

    cdef struct _GRBsvec:
        int len
        int* ind
        double* val

    ctypedef _GRBsvec GRBsvec

    int GRBFSolve(GRBmodel* model, GRBsvec* b, GRBsvec* x)

    int GRBBinvColj(GRBmodel* model, int j, GRBsvec* x)

    int GRBBinvj(GRBmodel* model, int j, GRBsvec* x)

    int GRBBSolve(GRBmodel* model, GRBsvec* b, GRBsvec* x)

    int GRBBinvi(GRBmodel* model, int i, GRBsvec* x)

    int GRBBinvRowi(GRBmodel* model, int i, GRBsvec* x)

    int GRBgetBasisHead(GRBmodel* model, int* bhead)

    int GRBstrongbranch(GRBmodel* model, int num, int* cand, double* downobjbd, double* upobjbd, int* statusP)

    int GRBcheckmodel(GRBmodel* model)

    void GRBsetsignal(GRBmodel* model)

    void GRBterminate(GRBmodel* model)

    int GRBreplay(char* filename)

    int GRBsetobjective(GRBmodel* model, int sense, double constant, int lnz, int* lind, double* lval, int qnz, int* qrow, int* qcol, double* qval)

    int GRBsetobjectiven(GRBmodel* model, int index, int priority, double weight, double abstol, double reltol, char* name, double constant, int lnz, int* lind, double* lval)

    void GRBclean2(int* lenP, int* ind, double* val)

    void GRBclean3(int* lenP, int* ind0, int* ind1, double* val)

    void GRBmsg(GRBenv* env, char* message)

    int GRBgetlogfile(GRBenv* env, FILE** logfileP)

    int GRBsetlogfile(GRBenv* env, FILE* logfile)

    int GRBgetintparam(GRBenv* env, char* paramname, int* valueP)

    int GRBgetdblparam(GRBenv* env, char* paramname, double* valueP)

    int GRBgetstrparam(GRBenv* env, char* paramname, char* valueP)

    int GRBgetintparaminfo(GRBenv* env, char* paramname, int* valueP, int* minP, int* maxP, int* defP)

    int GRBgetdblparaminfo(GRBenv* env, char* paramname, double* valueP, double* minP, double* maxP, double* defP)

    int GRBgetstrparaminfo(GRBenv* env, char* paramname, char* valueP, char* defP)

    int GRBsetparam(GRBenv* env, char* paramname, char* value)

    int GRBsetintparam(GRBenv* env, char* paramname, int value)

    int GRBsetdblparam(GRBenv* env, char* paramname, double value)

    int GRBsetstrparam(GRBenv* env, char* paramname, char* value)

    int GRBgetparamtype(GRBenv* env, char* paramname)

    int GRBresetparams(GRBenv* env)

    int GRBcopyparams(GRBenv* dest, GRBenv* src)

    int GRBwriteparams(GRBenv* env, char* filename)

    int GRBreadparams(GRBenv* env, char* filename)

    int GRBgetnumparams(GRBenv* env)

    int GRBgetparamname(GRBenv* env, int i, char** paramnameP)

    int GRBgetnumattributes(GRBmodel* model)

    int GRBgetattrname(GRBmodel* model, int i, char** attrnameP)

    int GRBloadenv(GRBenv** envP, char* logfilename)

    int GRBemptyenv(GRBenv** envP)

    int GRBemptyenvadv(GRBenv** envP, int apitype, int major, int minor, int tech)

    int GRBstartenv(GRBenv* env)

    ctypedef int (*_GRBloadenvadv_cb_ft)(GRBmodel* model, void* cbdata, int where, void* usrdata)

    int GRBloadenvadv(GRBenv** envP, char* logfilename, int apitype, int major, int minor, int tech, char* server, char* router, char* password, char* group, int priority, int idletimeout, char* accessid, char* secretkey, _GRBloadenvadv_cb_ft cb, void* usrdata)

    ctypedef int (*_GRBloadenvadv2_cb_ft)(GRBmodel* model, void* cbdata, int where, void* usrdata)

    ctypedef int (*_GRBloadenvadv2_logcb_ft)(char* msg)

    int GRBloadenvadv2(GRBenv** envP, char* logfilename, int apitype, int major, int minor, int tech, char* server, char* router, char* password, char* group, int priority, int idletimeout, char* accessid, char* secretkey, _GRBloadenvadv2_cb_ft cb, void* usrdata, _GRBloadenvadv2_logcb_ft logcb)

    int GRBloadclientenv(GRBenv** envP, char* logfilename, char* computeserver, char* router, char* password, char* group, int tls_insecure, int priority, double timeout)

    ctypedef int (*_GRBloadclientenvadv_cb_ft)(GRBmodel* model, void* cbdata, int where, void* usrdata)

    int GRBloadclientenvadv(GRBenv** envP, char* logfilename, char* computeserver, char* router, char* password, char* group, int tls_insecure, int priority, double timeout, int apitype, int major, int minor, int tech, _GRBloadclientenvadv_cb_ft cb, void* usrdata)

    int GRBloadcloudenv(GRBenv** envP, char* logfilename, char* accessID, char* secretKey, char* pool, int priority)

    ctypedef int (*_GRBloadcloudenvadv_cb_ft)(GRBmodel* model, void* cbdata, int where, void* usrdata)

    int GRBloadcloudenvadv(GRBenv** envP, char* logfilename, char* accessID, char* secretKey, char* pool, int priority, int apitype, int major, int minor, int tech, _GRBloadcloudenvadv_cb_ft cb, void* usrdata)

    GRBenv* GRBgetenv(GRBmodel* model)

    GRBenv* GRBgetconcurrentenv(GRBmodel* model, int num)

    void GRBdiscardconcurrentenvs(GRBmodel* model)

    GRBenv* GRBgetmultiobjenv(GRBmodel* model, int num)

    void GRBdiscardmultiobjenvs(GRBmodel* model)

    void GRBreleaselicense(GRBenv* env)

    void GRBfreeenv(GRBenv* env)

    char* GRBgeterrormsg(GRBenv* env)

    char* GRBgetmerrormsg(GRBmodel* model)

    void GRBversion(int* majorP, int* minorP, int* technicalP)

    char* GRBplatform()

    int GRBlisttokens()

    int GRBtunemodel(GRBmodel* model)

    int GRBtunemodels(int nummodels, GRBmodel** models, GRBmodel* ignore, GRBmodel* hint)

    int GRBgettuneresult(GRBmodel* model, int i)

    int GRBgettunelog(GRBmodel* model, int i, char** logP)

    int GRBtunemodeladv(GRBmodel* model, GRBmodel* ignore, GRBmodel* hint)

    int GRBsync(GRBmodel* model)

    int GRBpingserver(char* server, char* password)
