<template>
  <div id="app">  
    <div id="data">
      <div class="header">
        <p> ID </p>
        <p>Номер колеса</p>
        <p class='warn'>Предупреждение</p>
        <p>Подтверждение</p>
      </div>
      <div class="body">
        <div v-for="(koleso, index) in kolesa" :key="index">
          <p>{{ koleso.id }} </p>
          <p>{{ koleso.wheel_id }}</p>
          <p class='warn'>{{ koleso.warning }}</p>
          <button @click="event => addClass(event, koleso.wheel_id, index)">
            {{ koleso.isDelete ? 'Исправлено' : 'Исправлено?' }}
          </button>
        </div>
      </div>
    </div>
    <div id="status">
      <div class="dropdown" :class="isOpenTable ? 'actived' : ''">
        <button 
          class="dropbtn" 
          @click="isOpenTable = !isOpenTable"
        >
          Простои оборудования
        </button>
        <div class="dropdown-content">
          <div class="header">
            <p>Номер колеса</p>
            <p>Начало простоя</p>
            <p>Конец простоя</p>
          </div>
          <div class='body'>
            <div v-for="(prosto, index) in prostoy" :key="index">
              <p>{{ prosto.wheel_id }} </p>
              <p>{{ prosto.start_downtime }}</p>
              <p class='warn'>{{ prosto.end_downtime }}</p>
            </div>
          </div>
          </div>
        </div>
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
  #app {
    display: flex;
  }

  #data .header {
    display: flex;
    margin-bottom: 1rem;
  }

  #data .body > div {
    display: flex;
    margin-bottom: 1rem;
    align-items: center;
  }

  p   {
    width: 170px;
    padding: 10px 0;
    border-style: solid;
    border-color: black;
    border-width: 2px;
    margin-right: 7vh;
    margin-left: 6vh;
    text-align: center;
  }

  #data  button{
      background-color: red;
      color: aliceblue ;
      border-radius: 6px;
      border-style: solid;
      margin-right: 7vh;
      margin-left: 6vh;
      width: 170px;
      height: 50px;
  }

  button:active, 
  button.clicked { 
    background-color: green !important;
  }

  .warn{
    width: 20vh;
  }

  #status {
    border-left: solid;
    border-width: 0.5vh;
    width: 100%;
  }

  .dropbtn {
    background-color: #4CAF50;
    color: white;
    padding: 16px;
    font-size: 16px;
    border: none;
    margin-left: 27.5vh;
    width: 25vh;
    margin-bottom: 1rem;
  }

  .dropdown {
    /* position: absolute; */
    /* display: inline-block; */
    /* width: 60vh; */
    /* right: 20vh; */
  }

  .dropdown-content {
    display: none;
    font-weight: 200;
    width: 100%;
  }

  .dropdown-content .header {
    display: flex;
    justify-content: space-around;
    margin-bottom: 1rem;
  }

  .dropdown-content p{
    margin: 0;
    width: 180px;
  }

  /* .dropdown-content p {
    width: 19vh;
    height: 3vh;
    margin-left: 0;
    margin-right: 0;
  } */

  .dropdown-content .body > div{
    display: flex;
    flex-direction: row;
    justify-content: space-around;
    margin-bottom: 1rem;
  }

  .dropdown-content .body > div div{
    border: 0;
    font-weight: 400;
  }

  .dropdown:active .dropdown-content, 
  .actived .dropdown-content{
    display: block;
    }

  /* div div{
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


 */

</style>