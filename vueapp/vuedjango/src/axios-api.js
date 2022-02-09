import axios from 'axios'

const getAPI=  axios.create({
    baseURL:'http://localhost:8000/',
    timeout:60000,
})
export {getAPI}