/*
 * Copyright (c) The acados authors.
 *
 * This file is part of acados.
 *
 * Licensed under the 2-Clause BSD License.
 */


#ifndef cartesian_d27dd94aa4acc829_COST
#define cartesian_d27dd94aa4acc829_COST

#ifdef __cplusplus
extern "C" {
#endif


// Cost at initial shooting node

int cartesian_d27dd94aa4acc829_cost_ext_cost_0_fun(const real_t** arg, real_t** res, int* iw, real_t* w, void *mem);
int cartesian_d27dd94aa4acc829_cost_ext_cost_0_fun_work(int *, int *, int *, int *);
const int *cartesian_d27dd94aa4acc829_cost_ext_cost_0_fun_sparsity_in(int);
const int *cartesian_d27dd94aa4acc829_cost_ext_cost_0_fun_sparsity_out(int);
int cartesian_d27dd94aa4acc829_cost_ext_cost_0_fun_n_in(void);
int cartesian_d27dd94aa4acc829_cost_ext_cost_0_fun_n_out(void);

int cartesian_d27dd94aa4acc829_cost_ext_cost_0_fun_jac_hess(const real_t** arg, real_t** res, int* iw, real_t* w, void *mem);
int cartesian_d27dd94aa4acc829_cost_ext_cost_0_fun_jac_hess_work(int *, int *, int *, int *);
const int *cartesian_d27dd94aa4acc829_cost_ext_cost_0_fun_jac_hess_sparsity_in(int);
const int *cartesian_d27dd94aa4acc829_cost_ext_cost_0_fun_jac_hess_sparsity_out(int);
int cartesian_d27dd94aa4acc829_cost_ext_cost_0_fun_jac_hess_n_in(void);
int cartesian_d27dd94aa4acc829_cost_ext_cost_0_fun_jac_hess_n_out(void);

int cartesian_d27dd94aa4acc829_cost_ext_cost_0_fun_jac(const real_t** arg, real_t** res, int* iw, real_t* w, void *mem);
int cartesian_d27dd94aa4acc829_cost_ext_cost_0_fun_jac_work(int *, int *, int *, int *);
const int *cartesian_d27dd94aa4acc829_cost_ext_cost_0_fun_jac_sparsity_in(int);
const int *cartesian_d27dd94aa4acc829_cost_ext_cost_0_fun_jac_sparsity_out(int);
int cartesian_d27dd94aa4acc829_cost_ext_cost_0_fun_jac_n_in(void);
int cartesian_d27dd94aa4acc829_cost_ext_cost_0_fun_jac_n_out(void);









// Cost at path shooting node

int cartesian_d27dd94aa4acc829_cost_ext_cost_fun(const real_t** arg, real_t** res, int* iw, real_t* w, void *mem);
int cartesian_d27dd94aa4acc829_cost_ext_cost_fun_work(int *, int *, int *, int *);
const int *cartesian_d27dd94aa4acc829_cost_ext_cost_fun_sparsity_in(int);
const int *cartesian_d27dd94aa4acc829_cost_ext_cost_fun_sparsity_out(int);
int cartesian_d27dd94aa4acc829_cost_ext_cost_fun_n_in(void);
int cartesian_d27dd94aa4acc829_cost_ext_cost_fun_n_out(void);

int cartesian_d27dd94aa4acc829_cost_ext_cost_fun_jac_hess(const real_t** arg, real_t** res, int* iw, real_t* w, void *mem);
int cartesian_d27dd94aa4acc829_cost_ext_cost_fun_jac_hess_work(int *, int *, int *, int *);
const int *cartesian_d27dd94aa4acc829_cost_ext_cost_fun_jac_hess_sparsity_in(int);
const int *cartesian_d27dd94aa4acc829_cost_ext_cost_fun_jac_hess_sparsity_out(int);
int cartesian_d27dd94aa4acc829_cost_ext_cost_fun_jac_hess_n_in(void);
int cartesian_d27dd94aa4acc829_cost_ext_cost_fun_jac_hess_n_out(void);

int cartesian_d27dd94aa4acc829_cost_ext_cost_fun_jac(const real_t** arg, real_t** res, int* iw, real_t* w, void *mem);
int cartesian_d27dd94aa4acc829_cost_ext_cost_fun_jac_work(int *, int *, int *, int *);
const int *cartesian_d27dd94aa4acc829_cost_ext_cost_fun_jac_sparsity_in(int);
const int *cartesian_d27dd94aa4acc829_cost_ext_cost_fun_jac_sparsity_out(int);
int cartesian_d27dd94aa4acc829_cost_ext_cost_fun_jac_n_in(void);
int cartesian_d27dd94aa4acc829_cost_ext_cost_fun_jac_n_out(void);








// Cost at terminal shooting node

int cartesian_d27dd94aa4acc829_cost_ext_cost_e_fun(const real_t** arg, real_t** res, int* iw, real_t* w, void *mem);
int cartesian_d27dd94aa4acc829_cost_ext_cost_e_fun_work(int *, int *, int *, int *);
const int *cartesian_d27dd94aa4acc829_cost_ext_cost_e_fun_sparsity_in(int);
const int *cartesian_d27dd94aa4acc829_cost_ext_cost_e_fun_sparsity_out(int);
int cartesian_d27dd94aa4acc829_cost_ext_cost_e_fun_n_in(void);
int cartesian_d27dd94aa4acc829_cost_ext_cost_e_fun_n_out(void);

int cartesian_d27dd94aa4acc829_cost_ext_cost_e_fun_jac_hess(const real_t** arg, real_t** res, int* iw, real_t* w, void *mem);
int cartesian_d27dd94aa4acc829_cost_ext_cost_e_fun_jac_hess_work(int *, int *, int *, int *);
const int *cartesian_d27dd94aa4acc829_cost_ext_cost_e_fun_jac_hess_sparsity_in(int);
const int *cartesian_d27dd94aa4acc829_cost_ext_cost_e_fun_jac_hess_sparsity_out(int);
int cartesian_d27dd94aa4acc829_cost_ext_cost_e_fun_jac_hess_n_in(void);
int cartesian_d27dd94aa4acc829_cost_ext_cost_e_fun_jac_hess_n_out(void);

int cartesian_d27dd94aa4acc829_cost_ext_cost_e_fun_jac(const real_t** arg, real_t** res, int* iw, real_t* w, void *mem);
int cartesian_d27dd94aa4acc829_cost_ext_cost_e_fun_jac_work(int *, int *, int *, int *);
const int *cartesian_d27dd94aa4acc829_cost_ext_cost_e_fun_jac_sparsity_in(int);
const int *cartesian_d27dd94aa4acc829_cost_ext_cost_e_fun_jac_sparsity_out(int);
int cartesian_d27dd94aa4acc829_cost_ext_cost_e_fun_jac_n_in(void);
int cartesian_d27dd94aa4acc829_cost_ext_cost_e_fun_jac_n_out(void);









#ifdef __cplusplus
} /* extern "C" */
#endif

#endif  // cartesian_d27dd94aa4acc829_COST
