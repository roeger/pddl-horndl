tasks=(cat elevator task order trip tripv2)
# tasks=(cat elevator)
doupdate=1

if [ $doupdate -eq 1 ]; then
  csv="results_update.csv"
  rm -rf $csv
  echo "benchmark name,t closure,domain extension,collecting queries,rewriting,update rules const,gen derived preds,finalize,total complation,tseitin transformation, solution, size" >> $csv
else
  csv="results.csv"
  rm -rf $csv
  echo "benchmark name,collecting queries,rewriting,gen derived preds,finalize,total complation,tseitin transformation, solution, size" >> $csv
fi

for task in ${tasks[@]};
do
  if [ $task == "cat" ]; then
    elements=(6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25)
  elif [ $task == "elevator" ]; then
    elements=(15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34)
  elif [ $task == "task" ]; then
    elements=(3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22)
  else # order, trip, tripv2
    elements=(4 5 6 7 10 15 20 25 30 35 40 45 50 55 60)
  fi

  prefix="benchmarks/$task"
  ## path to a (patched) clipper
  clipper="/home/zinzin2312/repos/clipper/clipper-distribution/target/clipper/clipper.sh"
  nmo="/home/zinzin2312/repos/nemo/target/release/nmo"
  rls="code/nemo/t_closure.rls"
  fastdownward="/home/zinzin2312/repos/downward/fast-downward.py"
  # path to compiler.py
  compiler="code/compiler.py"
  tseitin="code/tseitin.py"

  owl=$prefix/original/TTL.owl
  input_domain=$prefix/original/domain.pddl

  for i in ${elements[@]};
  do
    input_problem="$prefix/original/${task}Problem${i}.pddl"

    # With update semantics
    if [ $doupdate -eq 1 ]; then
      result_domain="benchmarks/outputs/$task/domain_${i}.pddl"
      result_problem="benchmarks/outputs/$task/problem_${i}.pddl"
      tseitin_domain="benchmarks/outputs/$task/compiled_domain_${i}.pddl"
      tseitin_problem="benchmarks/outputs/$task/compiled_problem_${i}.pddl"

      echo "Compiling dom & prob $i with update"
      python3 "$compiler" "$owl" "$input_domain" "$input_problem" -d "$result_domain" -p "$result_problem" --clipper "$clipper" --clipper-mqf  --rls "$rls" --nmo "$nmo" --output-csv "$csv" --benchmark-name "$task $i"$@

      echo "Tseitin transformation $i"
      python3 "$tseitin" "$result_domain" "$result_problem" -d "$tseitin_domain" -p "$tseitin_problem" --keep-name  --keep-name --output-csv "$csv" --benchmark-name "$task $i"$@

      echo "Solving problem $i"
      # timeout 600 $fastdownward $domain $problem --evaluator "hcea=cea()" --search "lazy_greedy([hcea], preferred=[hcea])" > "benchmarks/outputs/$domain/solutions/solution${i}.txt" 2>&1
      planner_output=$(timeout 600 $fastdownward $tseitin_domain $tseitin_problem --evaluator "hcea=cea()" --search "lazy_greedy([hcea], preferred=[hcea])">&1)
      python helpers.py --output "$planner_output" --csv "$csv"
      echo "" >> $csv
    else
      result_domain="$prefix/pddl/domain_${i}.pddl"
      result_problem="$prefix/pddl/problem_${i}.pddl"
      tseitin_domain="$prefix/pddl/compiled_domain_${i}.pddl"
      tseitin_problem="$prefix/pddl/compiled_problem_${i}.pddl"

      echo "Compiling dom & prob $i"
      python3 "$compiler" "$owl" "$input_domain" "$input_problem" -d "$result_domain" -p "$result_problem" --clipper "$clipper" --clipper-mqf  --output-csv "$csv" --benchmark-name "$task $i"$@

      echo "Tseitin transformation $i"
      python3 "$tseitin" "$result_domain" "$result_problem" -d "$tseitin_domain" -p "$tseitin_problem" --keep-name --output-csv "$csv" --benchmark-name "$task $i"$@

      echo "Solving problem $i"
      # planner_output=$(timeout 600 $fastdownward $tseitin_domain $tseitin_problem --evaluator "hcea=cea()" --search "lazy_greedy([hcea], preferred=[hcea])">&1)
      planner_output=$(timeout 600 $fastdownward $tseitin_domain $tseitin_problem --heuristic "hff=ff(transform=adapt_costs(one))" --search "iterated([ehc(hff, preferred=[hff]), eager_greedy([hff], preferred=[hff])], continue_on_fail=true, continue_on_solve=false)">&1)

      python helpers.py --output "$planner_output" --csv "$csv"

      echo "" >> $csv
    fi
  done
done

rm -rf __temp_clipper_*
rm -rf sas_plan
