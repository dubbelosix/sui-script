import requests
import os
import json

state_query = '''{
    "jsonrpc":"2.0",
    "id":1,
    "method":"sui_getSuiSystemState"
}'''

checkpoint_metrics = '''{
    "jsonrpc":"2.0",
    "id":1,
    "method":"sui_getCheckpointSummary",
    "params":[%s, null, null, true]
}'''

latest_check = '''
   {"jsonrpc":"2.0", "id":1,"method":"sui_getLatestCheckpointSequenceNumber"}
'''

OVERCLOCK_ADDR = "0xaa10cfd6e38c4cf3ea1f7a99bd7c75b0a3d3f4c8"
FULLNODE_ADDR = "https://fullnode.testnet.sui.io"
EPOCH_LENGTH = 19000

def get_pending_addr_self_delegated_stake(lob,addr):
    for v in dat["result"]["validators"]["active_validators"]:
        if v["metadata"]["sui_address"] == addr:
            return (v["metadata"]["next_epoch_stake"], v["metadata"]["next_epoch_delegation"])

def get_pending_total_self_delegated_stake(lob):
    accumulator_self = 0
    accumulator_total = 0
    for v in dat["result"]["validators"]["active_validators"]:
        accumulator_self+=v["metadata"]["next_epoch_stake"]
        accumulator_total+=v["metadata"]["next_epoch_delegation"]
    return (accumulator_self, accumulator_total)

def get_current_gas_price(dat):
    return dat["result"]["reference_gas_price"]

def get_obj(query):
    f = requests.post(FULLNODE_ADDR, json=json.loads(query))
    dat = json.loads(f.text)
    return dat

if __name__ == "__main__":
    addr = os.getenv("ADDR") 
    if addr is None:
        addr = OVERCLOCK_ADDR
    dat = get_obj(state_query)
    (pending_clock_stake, pending_clock_delegation) = get_pending_addr_self_delegated_stake(dat,addr)
    (pending_total_stake, pending_total_delegation) = get_pending_total_self_delegated_stake(dat)
    print("pending validator self stake: %s MIST"%(pending_clock_stake))
    print("pending validator delegated stake: %s MIST"%(pending_clock_delegation))
    print("pending validator total stake: %s MIST"%(pending_clock_stake+pending_clock_delegation))
    print("----")
    print("pending everyone self stake: %s MIST"%(pending_total_stake))
    print("pending everyone delegated stake: %s MIST"%(pending_total_delegation))
    print("pending everyone total stake: %s MIST"%(pending_total_stake+pending_total_delegation))
    print("----")
    print("next epoch share: %.2f%%"%((pending_clock_stake+pending_clock_delegation)/(pending_total_stake+pending_total_delegation)*100))

    ref_gas_current = get_current_gas_price(dat)
    print("current gas price: %s"%ref_gas_current)

    dat = get_obj(latest_check)
    current_checkpoint = dat["result"]

    dat = get_obj(checkpoint_metrics%(current_checkpoint)) 
    current_epoch = dat["result"]["epoch"]
    current_epoch_cu = dat["result"]["epoch_rolling_gas_cost_summary"]["computation_cost"]
    current_epoch_sc = dat["result"]["epoch_rolling_gas_cost_summary"]["storage_cost"]
    current_epoch_sr = dat["result"]["epoch_rolling_gas_cost_summary"]["storage_rebate"]
    total_txns = dat["result"]["network_total_transactions"]
    prev_epoch = current_epoch - 1
    prev_checkpoint = (prev_epoch+1) * EPOCH_LENGTH

    curr_epoch_progress_percent = (current_checkpoint - int(current_checkpoint/19000) * 19000) / 19000 * 100

    dat = get_obj(checkpoint_metrics%(prev_checkpoint))
    prev_txns = dat["result"]["network_total_transactions"]
    curr_epoch_txns = total_txns - prev_txns
    print("----")
    print("current epoch progress = %.2f%%"%(curr_epoch_progress_percent))
    print("num txns so far: %s"%curr_epoch_txns)
    print("projected txn count: %s"%((curr_epoch_txns*100/curr_epoch_progress_percent)))
    print("current compute units per txn (excl storage) : %.4f"%(current_epoch_cu/curr_epoch_txns/ref_gas_current ))
    print("storage total: %s MIST"%(current_epoch_sc))
    print("storage rebate: %s MIST"%(current_epoch_sr))
