<template>
 <div class="propuestas">
    <h1 class="h1">Pagina de Listado de propuestas</h1>
    <button type="button" class="btn btn-primmary"><router-link :to="{name:'propuesta-crear'}">Agregar una nueva propuesta logica</router-link></button><br>
    <div class= "table-responsive">
        <table class="table table-bordered table-hover table-dark">
            <thead class="thead-dark">
            <tr>
                <td>ID </td>
                <td>Propuesta </td>
                <td>Respuesta </td>
            </tr>
            </thead>
            <tbody>
            <tr v-for="propuesta in propuestas">
                <td>{{propuesta.id}} </td>
                <td>{{propuesta.propuesta}} </td>
                <td>{{propuesta.respuesta}} </td>
            </tr>
            </tbody>
        </table>
    </div>
</div>
</template>
<script>
import axios from 'axios'
export default{
    mounted(){
        axios.get('http://127.0.0.1:8000/api/all/').then((respuesta)=>{
            this.propuestas=respuesta.data
        })

    },
    data(){
        return {
            propuestas:[]
        }
    }
}
</script>

