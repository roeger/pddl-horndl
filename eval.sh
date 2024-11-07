task="order"
## cat: 6 25
## elevator: 15 34
## task(assign): 3 22
## ============ Below uses elements ===========
## order(TPSA before):
## trip(VTA before):
## tripv2(VTA-roles before):
elements=(4 5 6 7 10 15 20 25 30 35 40 45 50 55 60)

fastdownward="/home/zinzin2312/repos/downward/fast-downward.py"

# for i in `seq 3 22`;
for i in ${elements[@]};
do
  # domain="benchmarks/outputs/$task/domain_${i}.pddl"
  # problem="benchmarks/outputs/$task/problem_${i}.pddl"
  domain="benchmarks/outputs/$task/compiled_domain_${i}.pddl"
  problem="benchmarks/outputs/$task/compiled_problem_${i}.pddl"

  echo "Solving problem $i"
  # timeout 600 $fastdownward $domain $problem --evaluator "hcea=cea()" --search "lazy_greedy([hcea], preferred=[hcea])" > "benchmarks/outputs/$domain/solutions/solution${i}.txt" 2>&1
  timeout 600 $fastdownward $domain $problem --evaluator "hcea=cea()" --search "lazy_greedy([hcea], preferred=[hcea])" > "benchmarks/outputs/$task/solutions/solution${i}.txt" 2>&1

  # $fastdownward $domain $problem --heuristic "hff=ff(transform=adapt_costs(one))" --search "iterated([ehc(hff, preferred=[hff]), eager_greedy([hff], preferred=[hff])], continue_on_fail=true, continue_on_solve=false)"
done
