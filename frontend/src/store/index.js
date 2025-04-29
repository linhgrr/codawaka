import { createStore } from 'vuex'
import axios from 'axios'
import apiConfig from '@/utils/apiConfig'

// API base URL
const API_URL = apiConfig.baseURL;

// Thiết lập token cho axios từ localStorage nếu có
const token = localStorage.getItem('token');
if (token) {
  axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
}

export default createStore({
  state: {
    token: localStorage.getItem('token') || '',
    user: JSON.parse(localStorage.getItem('user')) || null,
    credits: 0,
    models: [],
    codeHistory: [],
    paymentTransactions: []
  },
  getters: {
    isLoggedIn: state => !!state.token,
    isAdmin: state => state.user && state.user.is_admin,
    authStatus: state => state.status,
    currentUser: state => state.user,
    credits: state => state.credits,
    models: state => state.models,
    codeHistory: state => state.codeHistory,
    paymentTransactions: state => state.paymentTransactions
  },
  mutations: {
    AUTH_REQUEST(state) {
      state.status = 'loading'
    },
    AUTH_SUCCESS(state, { token, user }) {
      state.status = 'success'
      state.token = token
      state.user = user
    },
    AUTH_ERROR(state) {
      state.status = 'error'
    },
    LOGOUT(state) {
      state.status = ''
      state.token = ''
      state.user = null
      state.credits = 0
    },
    SET_CREDITS(state, credits) {
      state.credits = credits
    },
    SET_MODELS(state, models) {
      state.models = models
    },
    SET_CODE_HISTORY(state, history) {
      state.codeHistory = history
    },
    ADD_CODE_GENERATION(state, codeGen) {
      state.codeHistory.unshift(codeGen)
      // Update credits
      state.credits -= codeGen.credits_used
    },
    SET_PAYMENT_TRANSACTIONS(state, transactions) {
      state.paymentTransactions = transactions
    },
    ADD_PAYMENT_TRANSACTION(state, transaction) {
      state.paymentTransactions.unshift(transaction)
    },
    UPDATE_CREDITS_AFTER_PAYMENT(state, creditsAdded) {
      state.credits += creditsAdded
    }
  },
  actions: {
    login({ commit }, user) {
      return new Promise((resolve, reject) => {
        commit('AUTH_REQUEST')
        
        // Create form data for token endpoint
        const formData = new FormData()
        formData.append('username', user.username)
        formData.append('password', user.password)
        
        axios.post(`${API_URL}/token`, formData)
          .then(resp => {
            const token = resp.data.access_token
            
            // Store token in localStorage
            localStorage.setItem('token', token)
            
            // Set axios default Authorization header
            axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
            
            // Get user info with token
            axios.get(`${API_URL}/users/me`)
              .then(resp => {
                const user = resp.data
                localStorage.setItem('user', JSON.stringify(user))
                commit('AUTH_SUCCESS', { token, user })
                
                // Get user credits
                axios.get(`${API_URL}/users/me/credits`)
                  .then(resp => {
                    commit('SET_CREDITS', resp.data.credits)
                    resolve(resp)
                  })
                  .catch(err => {
                    console.error("Error fetching credits:", err)
                    resolve(resp)
                  })
              })
              .catch(err => {
                commit('AUTH_ERROR')
                localStorage.removeItem('token')
                reject(err)
              })
          })
          .catch(err => {
            commit('AUTH_ERROR')
            localStorage.removeItem('token')
            reject(err)
          })
      })
    },
    register({ commit }, user) {
      return new Promise((resolve, reject) => {
        axios.post(`${API_URL}/register`, user)
          .then(resp => {
            resolve(resp)
          })
          .catch(err => {
            reject(err)
          })
      })
    },
    logout({ commit }) {
      return new Promise((resolve) => {
        commit('LOGOUT')
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        delete axios.defaults.headers.common['Authorization']
        resolve()
      })
    },
    fetchCredits({ commit, state }) {
      if (!state.token) return Promise.reject(new Error('No authentication token'));
      
      return axios.get(`${API_URL}/users/me/credits`)
        .then(resp => {
          commit('SET_CREDITS', resp.data.credits);
          return resp.data.credits;
        })
        .catch(err => {
          console.error('Error fetching credits:', err);
          // Kiểm tra lỗi 401 để xử lý token hết hạn
          if (err.response && err.response.status === 401) {
            console.warn('Token expired or invalid');
            // Có thể thêm xử lý đăng xuất tự động ở đây nếu cần
          }
          throw err;
        });
    },
    fetchModels({ commit, state }) {
      if (!state.token) return
      
      return axios.get(`${API_URL}/models/`)
        .then(resp => {
          commit('SET_MODELS', resp.data)
          return resp
        })
    },
    fetchCodeHistory({ commit, state }, { page = 1, limit = 10 } = {}) {
      if (!state.token) return
      
      return axios.get(`${API_URL}/code/history?skip=${(page-1) * limit}&limit=${limit}`)
        .then(resp => {
          commit('SET_CODE_HISTORY', resp.data)
          return resp
        })
    },
    generateCode({ commit, state }, { model_name, prompt }) {
      if (!state.token) return
      
      return new Promise((resolve, reject) => {
        axios.post(`${API_URL}/code/generate-code`, { model_name, prompt })
          .then(resp => {
            commit('ADD_CODE_GENERATION', resp.data)
            resolve(resp.data)
          })
          .catch(err => {
            reject(err)
          })
      })
    },
    createPayment({ commit }, { credits }) {
      return new Promise((resolve, reject) => {
        // Đảm bảo token được thiết lập
        const token = localStorage.getItem('token');
        if (token) {
          axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        }
        
        axios.post(`${API_URL}/payment/create`, { credits })
          .then(resp => {
            resolve(resp.data);
          })
          .catch(err => {
            reject(err);
          });
      });
    },
    verifyPayment({ commit }, transactionId) {
      return new Promise((resolve, reject) => {
        // Đảm bảo token được thiết lập
        const token = localStorage.getItem('token');
        if (token) {
          axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        }
        
        // Kiểm tra nếu không có transaction ID hoặc ID không hợp lệ
        if (!transactionId || transactionId === '' || transactionId === '{paymentLinkId}') {
          console.warn('No valid transaction ID provided to verify');
          // Không reject promise, thay vào đó chúng ta sẽ lấy giao dịch gần nhất
          resolve(false);
          return;
        }
        
        axios.get(`${API_URL}/payment/verify/${transactionId}`)
          .then(resp => {
            if (resp.data) {
              // Payment was successful, refresh user credits
              axios.get(`${API_URL}/users/me/credits`)
                .then(creditsResp => {
                  commit('SET_CREDITS', creditsResp.data.credits);
                })
                .catch(err => {
                  console.error("Error fetching credits after payment:", err);
                });
            }
            resolve(resp.data);
          })
          .catch(err => {
            console.error('Payment verification failed:', err);
            reject(err);
          });
      });
    },
    
    // Thêm action mới để lấy và xác minh giao dịch gần nhất
    verifyLatestPayment({ commit, dispatch }) {
      return new Promise((resolve, reject) => {
        // Đảm bảo token được thiết lập
        const token = localStorage.getItem('token');
        if (token) {
          axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        }
        
        // Đầu tiên, lấy lịch sử thanh toán
        dispatch('fetchPaymentHistory')
          .then(transactions => {
            if (!transactions || transactions.length === 0) {
              resolve(false);
              return;
            }
            
            // Lấy giao dịch gần nhất
            const latestTransaction = transactions[0];
            console.log('Latest transaction:', latestTransaction);
            
            // Nếu giao dịch đã hoàn thành, không cần xác minh lại
            if (latestTransaction.status === 'completed') {
              // Cập nhật credits
              dispatch('fetchCredits');
              resolve(true);
              return;
            }
            
            // Xác minh giao dịch gần nhất
            dispatch('verifyPayment', latestTransaction.transaction_id)
              .then(result => {
                resolve(result);
              })
              .catch(err => {
                console.error('Error verifying latest transaction:', err);
                reject(err);
              });
          })
          .catch(err => {
            console.error('Error fetching payment history:', err);
            reject(err);
          });
      });
    },
    fetchPaymentHistory({ commit }, { page = 1, limit = 10 } = {}) {
      return new Promise((resolve, reject) => {
        // Đảm bảo token được thiết lập
        const token = localStorage.getItem('token');
        if (token) {
          axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        }
        
        axios.get(`${API_URL}/payment/history?skip=${(page-1) * limit}&limit=${limit}`)
          .then(resp => {
            commit('SET_PAYMENT_TRANSACTIONS', resp.data);
            resolve(resp.data);
          })
          .catch(err => {
            console.error('Failed to fetch payment history:', err);
            reject(err);
          });
      });
    },
    // Thêm hàm trợ giúp để khôi phục phiên đăng nhập
    restoreSession({ commit, dispatch }) {
      return new Promise((resolve, reject) => {
        const token = localStorage.getItem('token');
        const user = JSON.parse(localStorage.getItem('user'));
        
        if (!token || !user) {
          reject(new Error('No session data found'));
          return;
        }
        
        // Thiết lập token cho axios
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        
        // Kiểm tra token có hợp lệ hay không
        axios.get(`${API_URL}/users/me`)
          .then(resp => {
            // Cập nhật thông tin người dùng nếu cần
            const updatedUser = resp.data;
            localStorage.setItem('user', JSON.stringify(updatedUser));
            
            // Cập nhật store
            commit('AUTH_SUCCESS', { token, user: updatedUser });
            
            // Lấy thông tin credits
            dispatch('fetchCredits')
              .then(() => resolve(true))
              .catch(err => {
                console.error('Error fetching credits during session restore:', err);
                resolve(true); // Vẫn xem như thành công dù không lấy được credits
              });
          })
          .catch(err => {
            // Token không hợp lệ
            console.error('Failed to restore session:', err);
            commit('LOGOUT');
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            delete axios.defaults.headers.common['Authorization'];
            reject(err);
          });
      });
    }
  },
  modules: {
  }
})