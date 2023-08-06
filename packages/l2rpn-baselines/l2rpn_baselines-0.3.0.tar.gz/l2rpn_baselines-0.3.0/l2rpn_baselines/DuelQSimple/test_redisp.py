import grid2op
import pdb
env = grid2op.make("wcci_test")
amount = 1.0
gen_id = 8
gen_p = 1.
while gen_p > 0.:
  obs, reward, done, info = env.step(env.action_space())
  gen_p = obs.prod_p[gen_id]
# pdb.set_trace()
act = env.action_space({"redispatch": [(gen_id, amount)]})
obs, reward, done, info = env.step(act)
print(info)
print("gen p: {}".format(obs.prod_p[gen_id]))
print(obs.actual_dispatch)
