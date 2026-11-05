#
# Copyright (c) The acados authors.
#
# This file is part of acados.
#
# Licensed under the 2-Clause BSD License.





# define sources and use make's implicit rules to generate object files (*.o)

# model
MODEL_SRC=

MODEL_SRC+= cartesian_a8e5d797483d7e48_model/cartesian_a8e5d797483d7e48_dyn_disc_phi_fun.c
MODEL_SRC+= cartesian_a8e5d797483d7e48_model/cartesian_a8e5d797483d7e48_dyn_disc_phi_fun_jac.c
MODEL_SRC+= cartesian_a8e5d797483d7e48_model/cartesian_a8e5d797483d7e48_dyn_disc_phi_fun_jac_hess.c

MODEL_OBJ := $(MODEL_SRC:.c=.o)
# optimal control problem - mostly CasADi exports
OCP_SRC=


OCP_SRC+= cartesian_a8e5d797483d7e48_constraints/cartesian_a8e5d797483d7e48_constr_h_0_fun_jac_uxt_zt.c
OCP_SRC+= cartesian_a8e5d797483d7e48_constraints/cartesian_a8e5d797483d7e48_constr_h_0_fun_jac_uxt_zt_hess.c
OCP_SRC+= cartesian_a8e5d797483d7e48_constraints/cartesian_a8e5d797483d7e48_constr_h_0_fun.c
OCP_SRC+= cartesian_a8e5d797483d7e48_constraints/cartesian_a8e5d797483d7e48_constr_h_fun_jac_uxt_zt.c
OCP_SRC+= cartesian_a8e5d797483d7e48_constraints/cartesian_a8e5d797483d7e48_constr_h_fun_jac_uxt_zt_hess.c
OCP_SRC+= cartesian_a8e5d797483d7e48_constraints/cartesian_a8e5d797483d7e48_constr_h_fun.c
OCP_SRC+= cartesian_a8e5d797483d7e48_cost/cartesian_a8e5d797483d7e48_cost_ext_cost_0_fun.c
OCP_SRC+= cartesian_a8e5d797483d7e48_cost/cartesian_a8e5d797483d7e48_cost_ext_cost_0_fun_jac_hess.c
OCP_SRC+= cartesian_a8e5d797483d7e48_cost/cartesian_a8e5d797483d7e48_cost_ext_cost_0_fun_jac.c
OCP_SRC+= cartesian_a8e5d797483d7e48_cost/cartesian_a8e5d797483d7e48_cost_ext_cost_fun.c
OCP_SRC+= cartesian_a8e5d797483d7e48_cost/cartesian_a8e5d797483d7e48_cost_ext_cost_fun_jac_hess.c
OCP_SRC+= cartesian_a8e5d797483d7e48_cost/cartesian_a8e5d797483d7e48_cost_ext_cost_fun_jac.c
OCP_SRC+= cartesian_a8e5d797483d7e48_cost/cartesian_a8e5d797483d7e48_cost_ext_cost_e_fun.c
OCP_SRC+= cartesian_a8e5d797483d7e48_cost/cartesian_a8e5d797483d7e48_cost_ext_cost_e_fun_jac_hess.c
OCP_SRC+= cartesian_a8e5d797483d7e48_cost/cartesian_a8e5d797483d7e48_cost_ext_cost_e_fun_jac.c

OCP_SRC+= acados_solver_ocp_cartesian_a8e5d797483d7e48_7661a1d7.c

OCP_OBJ := $(OCP_SRC:.c=.o)
# for target example
EX_SRC= main_ocp_cartesian_a8e5d797483d7e48_7661a1d7.c
EX_OBJ := $(EX_SRC:.c=.o)
EX_EXE := $(EX_SRC:.c=)


# combine model, (potentially) sim and ocp object files
OBJ=
OBJ+= $(MODEL_OBJ)
OBJ+= $(OCP_OBJ)

EXTERNAL_DIR=
EXTERNAL_LIB=

INCLUDE_PATH = /home/yjh/projectlab_ws/third_party/acados/include
LIB_PATH = /home/yjh/projectlab_ws/third_party/acados/lib

# preprocessor flags for make's implicit rules
CPPFLAGS+= -I$(INCLUDE_PATH)
CPPFLAGS+= -I$(INCLUDE_PATH)/acados
CPPFLAGS+= -I$(INCLUDE_PATH)/blasfeo/include
CPPFLAGS+= -I$(INCLUDE_PATH)/hpipm/include


# define the c-compiler flags for make's implicit rules
CFLAGS = -fPIC -std=c99   -O2

# # Debugging
# CFLAGS += -g3 -fno-diagnostics-show-line-numbers -g

# linker flags
LDFLAGS+= -L$(LIB_PATH)


# link to libraries
LDLIBS+= -lacados
LDLIBS+= -lhpipm
LDLIBS+= -lblasfeo
LDLIBS+= -lm
LDLIBS+= 

# libraries
LIBACADOS_SOLVER=libacados_solver_ocp_cartesian_a8e5d797483d7e48_7661a1d7.so
LIBACADOS_OCP_SOLVER=libacados_ocp_solver_ocp_cartesian_a8e5d797483d7e48_7661a1d7.so

# virtual targets
.PHONY : all clean
all: clean example
shared_lib: ocp_shared_lib

# some linker targets
example: $(EX_OBJ) $(OBJ)
	$(CC) $^ -o $(EX_EXE) $(LDFLAGS) $(LDLIBS)


bundled_shared_lib: $(OBJ)
	$(CC) -shared $^ -o $(LIBACADOS_SOLVER) $(LDFLAGS) $(LDLIBS)

ocp_shared_lib: $(OCP_OBJ) $(MODEL_OBJ)
	$(CC) -shared $^ -o $(LIBACADOS_OCP_SOLVER) $(LDFLAGS) $(LDLIBS) \
	-L$(EXTERNAL_DIR) -l$(EXTERNAL_LIB)


# Cython targets
ocp_cython_c: ocp_shared_lib
	cython \
	-o acados_ocp_solver_pyx.c \
	-I $(INCLUDE_PATH)/../interfaces/acados_template/acados_template \
	$(INCLUDE_PATH)/../interfaces/acados_template/acados_template/acados_ocp_solver_pyx.pyx \
	-I /home/yjh/projectlab_ws/third_party/acados_generated/a8e5d797483d7e48/code \

ocp_cython_o: ocp_cython_c
	$(CC) $(ACADOS_FLAGS) -c -O2 \
	-fPIC \
	-DNPY_NO_DEPRECATED_API=NPY_1_7_API_VERSION \
	-o acados_ocp_solver_pyx.o \
	-I $(INCLUDE_PATH)/blasfeo/include/ \
	-I $(INCLUDE_PATH)/hpipm/include/ \
	-I $(INCLUDE_PATH) \
	-I /usr/lib/python3/dist-packages/numpy/core/include \
	-I /usr/include/python3.10 \
	acados_ocp_solver_pyx.c \

ocp_cython: ocp_cython_o
	$(CC) $(ACADOS_FLAGS) -shared \
	-o acados_ocp_solver_pyx.so \
	-Wl,-rpath=$(LIB_PATH) \
	acados_ocp_solver_pyx.o \
	$(abspath .)/libacados_ocp_solver_ocp_cartesian_a8e5d797483d7e48_7661a1d7.so \
	$(LDFLAGS) $(LDLIBS)




clean:
	$(RM) $(OBJ) $(EX_OBJ)
	$(RM) $(LIBACADOS_SOLVER) $(LIBACADOS_OCP_SOLVER)
	$(RM) $(EX_EXE)
clean_ocp_shared_lib:
	$(RM) $(LIBACADOS_OCP_SOLVER)
	$(RM) $(OCP_OBJ)

clean_ocp_cython:
	$(RM) libacados_ocp_solver_ocp_cartesian_a8e5d797483d7e48_7661a1d7.so
	$(RM) acados_solver_ocp_cartesian_a8e5d797483d7e48_7661a1d7.o
	$(RM) acados_ocp_solver_pyx.so
	$(RM) acados_ocp_solver_pyx.o


