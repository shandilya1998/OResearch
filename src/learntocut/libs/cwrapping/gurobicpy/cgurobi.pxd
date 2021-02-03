cdef extern from "gurobi_c.h":

    ctypedef _GRBmodel GRBmodel

    ctypedef _GRBenv GRBenv

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
