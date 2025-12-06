
"""난이도관련 변수만 모아놓은부분

1. 스파이크 간격 o
2. 초기 단선 개수 o
3. 스파이크 범위/미세변동 범위?? o
4. 불안정 상태일때 hp 줄어드는 범위/시간간격 o
5. 파이프 터지는 빈도?? o
6. 수리시간?? -->x
7. 철문개수? -->x
8. 드론 빈도?? o
9. Q/W변화량 더 적게?? o
"""

DIFFICULTY = {

    "EASY": {

        "PRESSURE_UPDATE_INTERVAL": 200,   
        "MIN_RANDOM_CHANGE": 1,
        "MAX_RANDOM_CHANGE": 3,

        "MIN_SPIKE_INTERVAL": 5000,      
        "MAX_SPIKE_INTERVAL": 7000,
        "MIN_SPIKE_CHANGE": 10,
        "MAX_SPIKE_CHANGE": 25,

        "BROKEN_LOW_CHANCE": 0.006,        
        "BROKEN_MID_CHANCE": 0.012,         
        "BROKEN_HIGH_CHANCE": 0.022,        

        "HP_DAMAGE": 3,                   
        "HP_DAMAGE_INTERVAL": 1500,        

        "BEGIN_BROKEN_CNT": 2,

        "DRONE_CHANCE": 0.15,            

        "PRESSURE_CONTROL_AMOUNT": 3,      
    },


    "HARD": {

        "PRESSURE_UPDATE_INTERVAL": 150,
        "MIN_RANDOM_CHANGE": 1,
        "MAX_RANDOM_CHANGE": 4,

        "MIN_SPIKE_INTERVAL": 4000,
        "MAX_SPIKE_INTERVAL": 6000,
        "MIN_SPIKE_CHANGE": 10,
        "MAX_SPIKE_CHANGE": 30,

        "BROKEN_LOW_CHANCE": 0.008,
        "BROKEN_MID_CHANCE": 0.015,
        "BROKEN_HIGH_CHANCE": 0.025,

        "HP_DAMAGE": 5,
        "HP_DAMAGE_INTERVAL": 1800,

        "BEGIN_BROKEN_CNT": 4,

        "DRONE_CHANCE": 0.10,     # EASY보다 확률 낮음

        "PRESSURE_CONTROL_AMOUNT": 2,
    },

}