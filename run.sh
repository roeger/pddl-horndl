task="cat"
## cat: 6 25
## elevator: 15 34
## task(assign): 3 22
## ============ Below uses elements ===========
## order(TPSA before):
## trip(VTA before):
## tripv2(VTA-roles before):
elements=(4 5 6 7 10 15 20 25 30 35 40 45 50 55 60)

prefix="benchmarks/$task"
## path to a (patched) clipper
clipper="/home/zinzin2312/repos/clipper/clipper-distribution/target/clipper/clipper.sh"
nmo="/home/zinzin2312/repos/nemo/target/release/nmo"
## laptop
# clipper="/home/zinzin2312/Desktop/repos/clipper/clipper-distribution/target/clipper/clipper.sh"
# nmo="/home/zinzin2312/Desktop/repos/nemo/target/release/nmo"

rls="code/nemo/t_closure.rls"

fastdownward="/home/zinzin2312/repos/downward/fast-downward.py"

# path to compiler.py
compiler="code/compiler.py"
tseitin="code/tseitin.py"

owl=$prefix/original/TTL.owl
input_domain=$prefix/original/domain.pddl

for i in `seq 6 25`;
# for i in ${elements[@]};
do
  input_problem="$prefix/original/${task}Problem${i}.pddl"

  # where the result should be written to
  result_domain="benchmarks/outputs/$task/domain_${i}.pddl"
  result_problem="benchmarks/outputs/$task/problem_${i}.pddl"
  tseitin_domain="benchmarks/outputs/$task/compiled_domain_${i}.pddl"
  tseitin_problem="benchmarks/outputs/$task/compiled_problem_${i}.pddl"

  # run compilation
  python3 "$compiler" "$owl" "$input_domain" "$input_problem" -d "$result_domain" -p "$result_problem" --clipper "$clipper" --clipper-mqf  --rls "$rls" --nmo "$nmo" --debug -v $@

  # run tseitin transformation
  python3 "$tseitin" "$result_domain" "$result_problem" -d "$tseitin_domain" -p "$tseitin_problem" -v --keep-name $@

  echo "Solving problem $i"
  # timeout 600 $fastdownward $domain $problem --evaluator "hcea=cea()" --search "lazy_greedy([hcea], preferred=[hcea])" > "benchmarks/outputs/$domain/solutions/solution${i}.txt" 2>&1
  timeout 600 $fastdownward $tseitin_domain $tseitin_problem --evaluator "hcea=cea()" --search "lazy_greedy([hcea], preferred=[hcea])" > "benchmarks/outputs/$task/solutions/solution${i}.txt" 2>&1
done

rm -rf __temp_clipper_*

