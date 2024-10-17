domain="cats"
prefix="benchmarks/$domain"
fastdownward="/home/zinzin2312/repos/downward/fast-downward.py"

for i in `seq 6 25`;
do
  tseitin_domain="benchmarks/outputs/$domain/compiled_domain${i}.pddl"

  tseitin_problem="benchmarks/outputs/$domain/compiled_problem${i}.pddl"

  echo "Solving problem $i"
  $fastdownward --alias lama-first $tseitin_domain $tseitin_problem  > "benchmarks/outputs/$domain/solution${i}.txt" 2>&1
done
