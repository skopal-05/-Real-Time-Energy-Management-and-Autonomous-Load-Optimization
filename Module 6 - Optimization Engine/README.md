# Module 6 - Optimization Engine

## Purpose

Module 6 improves the best operating scenario selected by Module 5 while
respecting the production, equipment, battery, and grid limits supplied by
Module 4 and the system state. It then converts the optimized operating state
into validated, actionable recommendations.

This implementation covers the complete Week 6 scope assigned to Person 1
and Person 2. The `integration/` controller and the cross-module end-to-end
test remain Person 3 responsibilities.

## Workflow

```text
Module 5 best scenario + Module 4 recommendations + system limits
                              |
                              v
                    OptimizationProblem
                              |
                              v
                 Real-valued Genetic Algorithm
                              |
                 objective + constraint checks
                              |
                              v
                    Optimized operating state
                              |
                              v
             Recommendation Engine and JSON reports
```

## Person 1 Components

- `algorithms/genetic_algorithm.py`: deterministic real-valued genetic
  algorithm with elitism, tournament selection, crossover, and mutation.
- `optimization/objective_function.py`: weighted energy, cost, and carbon
  objective using the Module 5 ranking weights (0.35, 0.35, 0.30).
- `optimization/constraints.py`: variable ranges, battery SOC, mutually
  exclusive charging/discharging, energy balance, and grid import limits.
- `optimization/optimizer.py`: converts input dictionaries into an
  optimization problem and returns the best feasible operating state.
- `optimization/optimization_validator.py`: validates inputs and results.

## Person 2 Components

- `recommendation/recommendation_engine.py`: compares baseline and optimized
  setpoints and produces actions, priorities, reasons, and expected impacts.
- `recommendation/recommendation_validator.py`: validates the recommendation
  schema, identifiers, priorities, and numeric values.
- `outputs/optimized_states/optimized_state.json`: optimized setpoints and
  algorithm details.
- `outputs/recommendations/recommendations.json`: actionable recommendations.
- `outputs/reports/optimization_report.json`: baseline-versus-optimized
  comparison and performance summary.

## Important Input Correction

The current Module 5 best scenario contains `production_load_kw: 0.0` because
Module 3 did not originally convert production units/hour into electrical
power. Module 4 does contain the required production target of `68.7 kW`.

The optimizer deliberately uses the Module 4 target and fixes production at
that value. It raises an error if both sources say production demand is zero.
This prevents the algorithm from reporting artificial savings by removing
production load.

## Objective

The Genetic Algorithm minimizes:

```text
0.35 * normalized primary energy
+ 0.35 * normalized operating cost
+ 0.30 * normalized carbon emissions
+ constraint violation penalties
```

The energy objective includes useful plant electrical demand, the energy
content of boiler fuel, and a penalty for curtailed renewable energy. Battery
charging is not treated as useful load, but is valuable when it absorbs solar
generation that cannot be exported. This prevents the optimizer from
artificially increasing equipment loads merely to consume surplus solar power.
Cost includes grid imports, fuel, battery degradation, and export revenue.
Carbon includes grid and boiler-fuel emissions.

## Running Tests

From the project root:

```bash
python3 -m unittest discover -s "Module 6 - Optimization Engine/tests" -v
```

## Person 3 Connection Contract

The future integration controller should:

1. Load Module 5 `best_scenario.json`.
2. Load Module 4 `recommendations.json` and `optimized_state.json`.
3. Pass the dictionaries to `Optimizer.build_problem(...)`.
4. Call `Optimizer.optimize(problem)`.
5. Pass the result to `RecommendationEngine.write_outputs(...)`.

The optimization and recommendation layers do not depend on hard-coded file
paths, so they can also be called from an API or a future Digital Twin service.
