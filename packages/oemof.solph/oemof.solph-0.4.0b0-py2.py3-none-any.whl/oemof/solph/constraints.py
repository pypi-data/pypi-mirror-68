# -*- coding: utf-8 -*-

"""Additional constraints to be used in an oemof energy model.
This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/oemof/solph/constraints.py

SPDX-License-Identifier: MIT
"""

import pyomo.environ as po
from oemof.solph.plumbing import sequence


def investment_limit(model, limit=None):
    r""" Set an absolute limit for the total investment costs of an investment
    optimization problem:

    .. math:: \sum_{investment\_costs} \leq limit

    Parameters
    ----------
    model : oemof.solph.Model
        Model to which the constraint is added
    limit : float
        Absolute limit of the investment (i.e. RHS of constraint)
    """

    def investment_rule(m):
        expr = 0

        if hasattr(m, "InvestmentFlow"):
            expr += m.InvestmentFlow.investment_costs

        if hasattr(m, "GenericInvestmentStorageBlock"):
            expr += m.GenericInvestmentStorageBlock.investment_costs
        return expr <= limit

    model.investment_limit = po.Constraint(rule=investment_rule)

    return model


def emission_limit(om, flows=None, limit=None):
    r"""
    Short handle for generic_integral_limit() with keyword="emission_factor".

    Note
    ----
    Flow objects required an attribute "emission_factor"!

    """
    generic_integral_limit(om,
                           keyword='emission_factor',
                           flows=flows,
                           limit=limit)


def generic_integral_limit(om, keyword, flows=None, limit=None):
    r"""Set a global limit for flows weighted by attribute called keyword.
    The attribute named by keyword has to be added
    to every flow you want to take into account.

    Total value of keyword attributes after optimization can be retrieved
    calling the :attr:`om.oemof.solph.Model.integral_limit_${keyword}()`.

    Parameters
    ----------
    om : oemof.solph.Model
        Model to which constraints are added.
    flows : dict
        Dictionary holding the flows that should be considered in constraint.
        Keys are (source, target) objects of the Flow. If no dictionary is
        given all flows containing the keyword attribute will be
        used.
    keyword : attribute to consider
    limit : numeric
        Absolute limit of keyword attribute for the energy system.

    Note
    ----
    Flow objects required an attribute named like keyword!

    **Constraint:**

    .. math:: \sum_{i \in F_E} \sum_{t \in T} P_i(t) \cdot w_i(t)
               \cdot \tau(t) \leq M


    With `F_I` being the set of flows considered for the integral limit and
    `T` being the set of time steps.

    The symbols used are defined as follows
    (with Variables (V) and Parameters (P)):

    ================ ==== =====================================================
    math. symbol     type explanation
    ================ ==== =====================================================
    :math:`P_n(t)`   V    power flow :math:`n` at time step :math:`t`
    :math:`w_N(t)`   P    weight given to Flow named according to `keyword`
    :math:`\tau(t)`  P    width of time step :math:`t`
    :math:`L`        P    global limit given by keyword `limit`
    ================ ==== =====================================================

    Examples
    --------
    >>> import pandas as pd
    >>> from oemof import solph
    >>> date_time_index = pd.date_range('1/1/2012', periods=5, freq='H')
    >>> energysystem = solph.EnergySystem(timeindex=date_time_index)
    >>> bel = solph.Bus(label='electricityBus')
    >>> flow1 = solph.Flow(nominal_value=100, my_factor=0.8)
    >>> flow2 = solph.Flow(nominal_value=50)
    >>> src1 = solph.Source(label='source1', outputs={bel: flow1})
    >>> src2 = solph.Source(label='source2', outputs={bel: flow2})
    >>> energysystem.add(bel, src1, src2)
    >>> model = solph.Model(energysystem)
    >>> flow_with_keyword = {(src1, bel): flow1, }
    >>> model = solph.constraints.generic_integral_limit(
    ...     model, "my_factor", flow_with_keyword, limit=777)
    """
    if flows is None:
        flows = {}
        for (i, o) in om.flows:
            if hasattr(om.flows[i, o], keyword):
                flows[(i, o)] = om.flows[i, o]

    else:
        for (i, o) in flows:
            if not hasattr(flows[i, o], keyword):
                raise AttributeError(
                    ('Flow with source: {0} and target: {1} '
                     'has no attribute {2}.').format(
                        i.label, o.label, keyword))

    limit_name = "integral_limit_"+keyword

    setattr(om, limit_name, po.Expression(
        expr=sum(om.flow[inflow, outflow, t]
                 * om.timeincrement[t]
                 * sequence(getattr(flows[inflow, outflow], keyword))[t]
                 for (inflow, outflow) in flows
                 for t in om.TIMESTEPS)))

    setattr(om, limit_name+"_constraint", po.Constraint(
        expr=(getattr(om, limit_name) <= limit)))

    return om


def limit_active_flow_count(model, constraint_name, flows,
                            lower_limit=0, upper_limit=None):
    r"""
    Set limits (lower and/or upper) for the number of concurrently
    active NonConvex flows. The flows are given as a list.

    Total actual counts after optimization can be retrieved
    calling the :attr:`om.oemof.solph.Model.$(constraint_name)_count()`.

    Parameters
    ----------
    model: oemof.solph.Model
        Model to which constraints are added
    constraint_name: string
        name for the constraint
    flows: list of flows
        flows (have to be NonConvex) in the format [(in, out)]
    lower_limit: integer
        minimum number of active flows in the list
    upper_limit: integer
        maximum number of active flows in the list

    Returns
    -------
    the updated model

    Note
    ----
    Flow objects required to be NonConvex

    **Constraint:**

    .. math:: N_{X,min} \le \sum_{n \in F} X_n(t)
                        \le N_{X,max} \forall t \in T

    With `F` being the set of considered flows and
    `T` being the set of time steps.

    The symbols used are defined as follows
    (with Variables (V) and Parameters (P)):

    ================== ==== ===================================================
    math. symbol       type explanation
    ================== ==== ===================================================
    :math:`X_n(t)`     V    status (0 or 1) of the flow :math:`n`
                            at time step :math:`t`
    :math:`N_{X,min}`  P    lower_limit
    :math:`N_{X,max}`  P    lower_limit
    ================== ==== ===================================================
    """

    # number of concurrent active flows
    setattr(model, constraint_name, po.Var(model.TIMESTEPS))

    for t in model.TIMESTEPS:
        getattr(model, constraint_name)[t].setlb(lower_limit)
        getattr(model, constraint_name)[t].setub(upper_limit)

    attrname_constraint = constraint_name + "_constraint"

    def _flow_count_rule(m):
        for ts in m.TIMESTEPS:
            lhs = sum(m.NonConvexFlow.status[fi, fo, ts]
                      for fi, fo in flows)
            rhs = getattr(model, constraint_name)[ts]
            expr = (lhs == rhs)
            if expr is not True:
                getattr(m, attrname_constraint).add(ts, expr)

    setattr(model, attrname_constraint,
            po.Constraint(model.TIMESTEPS, noruleinit=True))
    setattr(model, attrname_constraint+"_build",
            po.BuildAction(rule=_flow_count_rule))

    return model


def limit_active_flow_count_by_keyword(model, keyword,
                                       lower_limit=0, upper_limit=None):
    r"""
    This wrapper for limit_active_flow_count allows to set limits
    to the count of concurrently active flows by using a keyword
    instead of a list. The constraint will be named $(keyword)_count.

    Parameters
    ----------
    model: oemof.solph.Model
        Model to which constraints are added
    keyword: string
        keyword to consider (searches all NonConvexFlows)
    lower_limit: integer
        minimum number of active flows having the keyword
    upper_limit: integer
        maximum number of active flows having the keyword

    Returns
    -------
    the updated model

    See Also
    --------
    limit_active_flow_count(model, constraint_name, flows,
                            lower_limit=0, upper_limit=None)
    """
    flows = []
    for (i, o) in model.NonConvexFlow.NONCONVEX_FLOWS:
        if hasattr(model.flows[i, o], keyword):
            flows.append((i, o))

    return limit_active_flow_count(model, keyword,
                                   flows=flows,
                                   lower_limit=lower_limit,
                                   upper_limit=upper_limit)


def equate_variables(model, var1, var2, factor1=1, name=None):
    r"""
    Adds a constraint to the given model that set two variables to equal
    adaptable by a factor.

    **The following constraints are build:**

      .. math::
        var\textit{1} \cdot factor\textit{1} = var\textit{2}

    Parameters
    ----------
    var1 : pyomo.environ.Var
        First variable, to be set to equal with Var2 and multiplied with
        factor1.
    var2 : pyomo.environ.Var
        Second variable, to be set equal to (Var1 * factor1).
    factor1 : float
        Factor to define the proportion between the variables.
    name : str
        Optional name for the equation e.g. in the LP file. By default the
        name is: equate + string representation of var1 and var2.
    model : oemof.solph.Model
        Model to which the constraint is added.

    Examples
    --------
    The following example shows how to define a transmission line in the
    investment mode by connecting both investment variables. Note that the
    equivalent periodical costs (epc) of the line are 40. You could also add
    them to one line and set them to 0 for the other line.

    >>> import pandas as pd
    >>> from oemof import solph
    >>> date_time_index = pd.date_range('1/1/2012', periods=5, freq='H')
    >>> energysystem = solph.EnergySystem(timeindex=date_time_index)
    >>> bel1 = solph.Bus(label='electricity1')
    >>> bel2 = solph.Bus(label='electricity2')
    >>> energysystem.add(bel1, bel2)
    >>> energysystem.add(solph.Transformer(
    ...    label='powerline_1_2',
    ...    inputs={bel1: solph.Flow()},
    ...    outputs={bel2: solph.Flow(
    ...        investment=solph.Investment(ep_costs=20))}))
    >>> energysystem.add(solph.Transformer(
    ...    label='powerline_2_1',
    ...    inputs={bel2: solph.Flow()},
    ...   outputs={bel1: solph.Flow(
    ...       investment=solph.Investment(ep_costs=20))}))
    >>> om = solph.Model(energysystem)
    >>> line12 = energysystem.groups['powerline_1_2']
    >>> line21 = energysystem.groups['powerline_2_1']
    >>> solph.constraints.equate_variables(
    ...    om,
    ...    om.InvestmentFlow.invest[line12, bel2],
    ...    om.InvestmentFlow.invest[line21, bel1])
    """
    if name is None:
        name = '_'.join(["equate", str(var1), str(var2)])

    def equate_variables_rule(m):
        return var1 * factor1 == var2
    setattr(model, name, po.Constraint(rule=equate_variables_rule))
