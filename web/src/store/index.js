import Vue from 'vue'
import Vuex from 'vuex'
import auth from './modules/auth.store'

Vue.use(Vuex)

const store = new Vuex.Store({
    modules: {
        auth,
    },
    state: {},
    actions: {},
    mutations: {},
    getters: {},
})

export default store