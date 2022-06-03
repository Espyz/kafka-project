<template>
  <div id="app">    
    <div v-for="(koleso, index) in kolesa" :key="index">
      <p>{{ koleso.id }} {{ koleso.warning }} {{ koleso.wheel_id }}</p>
      <button @click="event => addClass(event, koleso.id, index)">
        {{ koleso.isDelete ? 'Confirm' : 'Confirm?' }}
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
      kolesa: []
    }
  },

  async mounted() {
    const response = await axios.get('/api/front-end');

    for (let i = 0; i < response.data.result.length; i++) {
      response.data.result[i].isDelete = false;
    }

    this.kolesa = response.data.result;
  },

  methods: {
    async addClass(event, id, index) {
      try {
        const response =  await axios.post('/api/back/', { id:  id });
        if (response.data.success) {
          event.target.classList.add('clicked');
          this.kolesa[index].isDelete = true;
        }
      }
      catch(err) {
        console.error(err);
      }
    }
  }
}
</script>

<style scoped>
  div div{
    color: black ;
    font-weight: bolder;
    flex-direction: row;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-wrap: wrap;
      }

  p   {
    width: 50vh;
    border-style: solid;
    border-color: black;
    border-width: 2px;
    margin-top:0.7vh;
    margin-right: 7vh;
    margin-left: 30vh;
    margin-bottom: 0.7vh ;
    text-align: center;
      }

  button{
      margin-right: 46vh;
      background-color: red;
      color: aliceblue ;
      border-radius: 6px;
      border-style: solid;
        }

button:active, 
button.clicked { 
  background-color: green;
}
</style>