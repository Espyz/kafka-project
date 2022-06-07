<template>
  <div id="app">  
    <p> ID </p>
    <p>Номер колеса</p>
    <p class='warn'>Предупреждение</p>
    <p>Подтверждение</p>
    <div class="dropdown" :class="isOpenTable ? 'actived' : ''">
      <button 
        class="dropbtn" 
        @click="isOpenTable = !isOpenTable"
      >
        Простои оборудования
      </button>
      <div class="dropdown-content">
        <div>
          <p>Номер колеса</p>
          <p>Начало простоя</p>
          <p>Конец простоя</p>
          <div v-for="(prosto, index) in prostoy" :key="index">
            <p>{{ prosto.wheel_id }} </p>
            <p>{{ prosto.start_downtime }}</p>
            <p class='warn'>{{ prosto.end_downtime }}</p>
          </div>
        </div>
      </div>
    </div> 
    <div v-for="(koleso, index) in kolesa" :key="index">
      <p>{{ koleso.id }} </p>
      <p>{{ koleso.wheel_id }}</p>
      <p class='warn'>{{ koleso.warning }}</p>
      <button @click="event => addClass(event, koleso.wheel_id, index)">
        {{ koleso.isDelete ? 'Исправлено' : 'Исправлено?' }}
      </button>
    </div>
  </div>
</template>


<script>
import axios from 'axios';

export default {
  name: 'app' ,

  data() {
    return {
      kolesa: [],
      isOpenTable: false,
    }
  },

  async mounted() {
    const response = await axios.get('/api/front-end-events');

    for (let i = 0; i < response.data.result.length; i++) {
      response.data.result[i].isDelete = false;
    }

    this.kolesa = response.data.result;

    const retponse = await axios.get('/api/front-end-idle');
    this.prostoy = retponse.data.result;
  },

  methods: {
    async addClass(event, wheel_id, index) {
      try {
        const response =  await axios.post('/api/back/', { wheel_id:  wheel_id });
        if (response.data.success) {
          event.target.classList.add('clicked');
          this.kolesa[index].isDelete = true;
        }
      }
      catch(err) {
        console.error(err);
      }
    },
  }
}
</script>

<style scoped>
  div div{
    margin-left: 10vh;
    flex-direction: row;
    display: flex; 
    flex-wrap: wrap;
  } 
  div div div{
    margin-left: 0;
    color: black ;
    font-weight: bolder;
    justify-content: center;
    align-items: center;
      }

  p   {
    width: 17vh;
    height: 6vh;
    border-style: solid;
    border-color: black;
    border-width: 2px;
    margin-top:0.7vh;
    margin-right: 7vh;
    margin-left: 6vh;
    margin-bottom: 0.7vh ;
    text-align: center;
      }

  button{
      margin-right: 40vh;
      background-color: red;
      color: aliceblue ;
      border-radius: 6px;
      border-style: solid;
      margin-left: 8vh;
        }

  .warn{
    width: 20vh;
  }

button:active, 
button.clicked { 
  background-color: green;
}

.dropbtn {
  background-color: #4CAF50;
  color: white;
  padding: 16px;
  font-size: 16px;
  border: none;
  margin-left: 27.5vh;
  width: 25vh;
}
.dropdown {
  position: absolute;
  display: inline-block;
  width: 60vh;
  right: 20vh;
}

.dropdown-content {
  display: none;
  font-weight: 200;
  }

.dropdown-content p {
  width: 19vh;
  height: 3vh;
  margin-left: 0;
  margin-right: 0;
}

.dropdown-content div{
  display: flex;
  flex-direction: row;
  border-left: solid;
  border-width: 0.5vh;
  justify-content: space-around;
  width: 80vh;
}

.dropdown-content div div{
  border: 0;
  font-weight: 400;
}

.dropdown:active .dropdown-content, 
.actived .dropdown-content{
  display: block;
  }

</style>