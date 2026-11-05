/*
 * Copyright (c) The acados authors.
 *
 * This file is part of acados.
 *
 * Licensed under the 2-Clause BSD License.
 */

#ifndef ACADOS_SOLVER_ocp_cartesian_6477a3441fc6bffa_984f769c_H_
#define ACADOS_SOLVER_ocp_cartesian_6477a3441fc6bffa_984f769c_H_

#include "acados/utils/types.h"

#include "acados_c/ocp_nlp_interface.h"
#include "acados_c/external_function_interface.h"

#define OCP_CARTESIAN_6477A3441FC6BFFA_984F769C_NX     6
#define OCP_CARTESIAN_6477A3441FC6BFFA_984F769C_NZ     0
#define OCP_CARTESIAN_6477A3441FC6BFFA_984F769C_NU     2
#define OCP_CARTESIAN_6477A3441FC6BFFA_984F769C_NP     11
#define OCP_CARTESIAN_6477A3441FC6BFFA_984F769C_NP_GLOBAL     0
#define OCP_CARTESIAN_6477A3441FC6BFFA_984F769C_NBX    0
#define OCP_CARTESIAN_6477A3441FC6BFFA_984F769C_NBX0   6
#define OCP_CARTESIAN_6477A3441FC6BFFA_984F769C_NBU    0
#define OCP_CARTESIAN_6477A3441FC6BFFA_984F769C_NSBX   0
#define OCP_CARTESIAN_6477A3441FC6BFFA_984F769C_NSBU   0
#define OCP_CARTESIAN_6477A3441FC6BFFA_984F769C_NSH    0
#define OCP_CARTESIAN_6477A3441FC6BFFA_984F769C_NSH0   0
#define OCP_CARTESIAN_6477A3441FC6BFFA_984F769C_NSG    0
#define OCP_CARTESIAN_6477A3441FC6BFFA_984F769C_NSPHI  0
#define OCP_CARTESIAN_6477A3441FC6BFFA_984F769C_NSHN   0
#define OCP_CARTESIAN_6477A3441FC6BFFA_984F769C_NSGN   0
#define OCP_CARTESIAN_6477A3441FC6BFFA_984F769C_NSPHIN 0
#define OCP_CARTESIAN_6477A3441FC6BFFA_984F769C_NSPHI0 0
#define OCP_CARTESIAN_6477A3441FC6BFFA_984F769C_NSBXN  0
#define OCP_CARTESIAN_6477A3441FC6BFFA_984F769C_NS     0
#define OCP_CARTESIAN_6477A3441FC6BFFA_984F769C_NS0    0
#define OCP_CARTESIAN_6477A3441FC6BFFA_984F769C_NSN    0
#define OCP_CARTESIAN_6477A3441FC6BFFA_984F769C_NG     0
#define OCP_CARTESIAN_6477A3441FC6BFFA_984F769C_NBXN   0
#define OCP_CARTESIAN_6477A3441FC6BFFA_984F769C_NGN    0
#define OCP_CARTESIAN_6477A3441FC6BFFA_984F769C_NY0    0
#define OCP_CARTESIAN_6477A3441FC6BFFA_984F769C_NY     0
#define OCP_CARTESIAN_6477A3441FC6BFFA_984F769C_NYN    0
#define OCP_CARTESIAN_6477A3441FC6BFFA_984F769C_N      20
#define OCP_CARTESIAN_6477A3441FC6BFFA_984F769C_NH     3
#define OCP_CARTESIAN_6477A3441FC6BFFA_984F769C_NHN    0
#define OCP_CARTESIAN_6477A3441FC6BFFA_984F769C_NH0    3
#define OCP_CARTESIAN_6477A3441FC6BFFA_984F769C_NPHI0  0
#define OCP_CARTESIAN_6477A3441FC6BFFA_984F769C_NPHI   0
#define OCP_CARTESIAN_6477A3441FC6BFFA_984F769C_NPHIN  0
#define OCP_CARTESIAN_6477A3441FC6BFFA_984F769C_NR     0

#ifdef __cplusplus
extern "C" {
#endif


// ** capsule for solver data **
typedef struct ocp_cartesian_6477a3441fc6bffa_984f769c_solver_capsule
{
    // acados objects
    ocp_nlp_in *nlp_in;
    ocp_nlp_out *nlp_out;
    ocp_nlp_out *sens_out;
    ocp_nlp_solver *nlp_solver;
    void *nlp_opts;
    ocp_nlp_plan_t *nlp_solver_plan;
    ocp_nlp_config *nlp_config;
    ocp_nlp_dims *nlp_dims;

    // number of expected runtime parameters
    unsigned int nlp_np;

    /* external functions */

    // dynamics

    external_function_external_param_casadi *discr_dyn_phi_fun;
    external_function_external_param_casadi *discr_dyn_phi_fun_jac_ut_xt;



    external_function_external_param_casadi *discr_dyn_phi_fun_jac_ut_xt_hess;


    // cost

    external_function_external_param_casadi *ext_cost_fun;
    external_function_external_param_casadi *ext_cost_fun_jac;
    external_function_external_param_casadi *ext_cost_fun_jac_hess;






    external_function_external_param_casadi ext_cost_0_fun;
    external_function_external_param_casadi ext_cost_0_fun_jac;
    external_function_external_param_casadi ext_cost_0_fun_jac_hess;





    external_function_external_param_casadi ext_cost_e_fun;
    external_function_external_param_casadi ext_cost_e_fun_jac;
    external_function_external_param_casadi ext_cost_e_fun_jac_hess;




    // constraints
    external_function_external_param_casadi *nl_constr_h_fun_jac;
    external_function_external_param_casadi *nl_constr_h_fun;
    external_function_external_param_casadi *nl_constr_h_fun_jac_hess;






    external_function_external_param_casadi nl_constr_h_0_fun_jac;
    external_function_external_param_casadi nl_constr_h_0_fun;
    external_function_external_param_casadi nl_constr_h_0_fun_jac_hess;







} ocp_cartesian_6477a3441fc6bffa_984f769c_solver_capsule;

ACADOS_SYMBOL_EXPORT ocp_cartesian_6477a3441fc6bffa_984f769c_solver_capsule * ocp_cartesian_6477a3441fc6bffa_984f769c_acados_create_capsule(void);
ACADOS_SYMBOL_EXPORT int ocp_cartesian_6477a3441fc6bffa_984f769c_acados_free_capsule(ocp_cartesian_6477a3441fc6bffa_984f769c_solver_capsule *capsule);

ACADOS_SYMBOL_EXPORT int ocp_cartesian_6477a3441fc6bffa_984f769c_acados_create(ocp_cartesian_6477a3441fc6bffa_984f769c_solver_capsule * capsule);

ACADOS_SYMBOL_EXPORT int ocp_cartesian_6477a3441fc6bffa_984f769c_acados_reset(ocp_cartesian_6477a3441fc6bffa_984f769c_solver_capsule* capsule, int reset_qp_solver_mem, int reset_numerical_values, int reset_solver_options, int reset_x_to_x0_bar);

/**
 * Generic version of ocp_cartesian_6477a3441fc6bffa_984f769c_acados_create which allows to use a different number of shooting intervals than
 * the number used for code generation. If new_time_steps=NULL and n_time_steps matches the number used for code
 * generation, the time-steps from code generation is used.
 */
ACADOS_SYMBOL_EXPORT int ocp_cartesian_6477a3441fc6bffa_984f769c_acados_create_with_discretization(ocp_cartesian_6477a3441fc6bffa_984f769c_solver_capsule * capsule, int n_time_steps, double* new_time_steps);
/**
 * Update the time step vector. Number N must be identical to the currently set number of shooting nodes in the
 * nlp_solver_plan. Returns 0 if no error occurred and a otherwise a value other than 0.
 */
ACADOS_SYMBOL_EXPORT int ocp_cartesian_6477a3441fc6bffa_984f769c_acados_update_time_steps(ocp_cartesian_6477a3441fc6bffa_984f769c_solver_capsule * capsule, int N, double* new_time_steps);
/**
 * This function is used for updating an already initialized solver with a different number of qp_cond_N.
 */
ACADOS_SYMBOL_EXPORT int ocp_cartesian_6477a3441fc6bffa_984f769c_acados_update_qp_solver_cond_N(ocp_cartesian_6477a3441fc6bffa_984f769c_solver_capsule * capsule, int qp_solver_cond_N);
ACADOS_SYMBOL_EXPORT int ocp_cartesian_6477a3441fc6bffa_984f769c_acados_update_params(ocp_cartesian_6477a3441fc6bffa_984f769c_solver_capsule * capsule, int stage, double *value, int np);
ACADOS_SYMBOL_EXPORT int ocp_cartesian_6477a3441fc6bffa_984f769c_acados_update_params_sparse(ocp_cartesian_6477a3441fc6bffa_984f769c_solver_capsule * capsule, int stage, int *idx, double *p, int n_update);
ACADOS_SYMBOL_EXPORT int ocp_cartesian_6477a3441fc6bffa_984f769c_acados_set_p_global_and_precompute_dependencies(ocp_cartesian_6477a3441fc6bffa_984f769c_solver_capsule* capsule, double* data, int data_len);

ACADOS_SYMBOL_EXPORT int ocp_cartesian_6477a3441fc6bffa_984f769c_acados_solve(ocp_cartesian_6477a3441fc6bffa_984f769c_solver_capsule * capsule);
ACADOS_SYMBOL_EXPORT int ocp_cartesian_6477a3441fc6bffa_984f769c_acados_setup_qp_matrices_and_factorize(ocp_cartesian_6477a3441fc6bffa_984f769c_solver_capsule* capsule);



ACADOS_SYMBOL_EXPORT int ocp_cartesian_6477a3441fc6bffa_984f769c_acados_free(ocp_cartesian_6477a3441fc6bffa_984f769c_solver_capsule * capsule);
ACADOS_SYMBOL_EXPORT void ocp_cartesian_6477a3441fc6bffa_984f769c_acados_print_stats(ocp_cartesian_6477a3441fc6bffa_984f769c_solver_capsule * capsule);
ACADOS_SYMBOL_EXPORT int ocp_cartesian_6477a3441fc6bffa_984f769c_acados_custom_update(ocp_cartesian_6477a3441fc6bffa_984f769c_solver_capsule* capsule, double* data, int data_len);

ACADOS_SYMBOL_EXPORT ocp_nlp_in *ocp_cartesian_6477a3441fc6bffa_984f769c_acados_get_nlp_in(ocp_cartesian_6477a3441fc6bffa_984f769c_solver_capsule * capsule);
ACADOS_SYMBOL_EXPORT ocp_nlp_out *ocp_cartesian_6477a3441fc6bffa_984f769c_acados_get_nlp_out(ocp_cartesian_6477a3441fc6bffa_984f769c_solver_capsule * capsule);
ACADOS_SYMBOL_EXPORT ocp_nlp_out *ocp_cartesian_6477a3441fc6bffa_984f769c_acados_get_sens_out(ocp_cartesian_6477a3441fc6bffa_984f769c_solver_capsule * capsule);
ACADOS_SYMBOL_EXPORT ocp_nlp_solver *ocp_cartesian_6477a3441fc6bffa_984f769c_acados_get_nlp_solver(ocp_cartesian_6477a3441fc6bffa_984f769c_solver_capsule * capsule);
ACADOS_SYMBOL_EXPORT ocp_nlp_config *ocp_cartesian_6477a3441fc6bffa_984f769c_acados_get_nlp_config(ocp_cartesian_6477a3441fc6bffa_984f769c_solver_capsule * capsule);
ACADOS_SYMBOL_EXPORT void *ocp_cartesian_6477a3441fc6bffa_984f769c_acados_get_nlp_opts(ocp_cartesian_6477a3441fc6bffa_984f769c_solver_capsule * capsule);
ACADOS_SYMBOL_EXPORT ocp_nlp_dims *ocp_cartesian_6477a3441fc6bffa_984f769c_acados_get_nlp_dims(ocp_cartesian_6477a3441fc6bffa_984f769c_solver_capsule * capsule);
ACADOS_SYMBOL_EXPORT ocp_nlp_plan_t *ocp_cartesian_6477a3441fc6bffa_984f769c_acados_get_nlp_plan(ocp_cartesian_6477a3441fc6bffa_984f769c_solver_capsule * capsule);

#ifdef __cplusplus
} /* extern "C" */
#endif

#endif  // ACADOS_SOLVER_ocp_cartesian_6477a3441fc6bffa_984f769c_H_
