import { defineStore } from 'pinia'
import { ref } from 'vue'
import request from '@/utils/request'
import { supabase } from '@/utils/supabase'

export interface UserInfo {
  id: string
  username: string
  email: string
  role: string
}

export const useUserStore = defineStore('user', () => {
  const token = ref<string>(localStorage.getItem('token') || '')
  const userInfo = ref<UserInfo>({
    id: '',
    username: '',
    email: '',
    role: ''
  })
  const isLoggedIn = ref<boolean>(!!token.value)

  // 登录
  const login = async (username: string, password: string) => {
    try {
      // 使用后端API进行登录验证
      const response = await request.post('/api/auth/login', {
        username,
        password
      })
      
      if (response.data.success) {
        token.value = response.data.data.token
        userInfo.value = response.data.data.user
        isLoggedIn.value = true
        localStorage.setItem('token', token.value)
        
        // 可选：同时登录到Supabase（如果需要使用Supabase的实时功能）
        // const { error } = await supabase.auth.signInWithPassword({
        //   email: userInfo.value.email,
        //   password: password
        // })
        
        return { success: true }
      } else {
        return { success: false, message: response.data.message }
      }
    } catch (error: any) {
      console.error('Login error:', error)
      return { 
        success: false, 
        message: error.response?.data?.message || '登录失败，请稍后重试' 
      }
    }
  }

  // 退出登录
  const logout = async () => {
    try {
      // 清理本地状态
      token.value = ''
      userInfo.value = {
        id: '',
        username: '',
        email: '',
        role: ''
      }
      isLoggedIn.value = false
      localStorage.removeItem('token')
      
      // 可选：同时从Supabase登出
      // await supabase.auth.signOut()
    } catch (error) {
      console.error('Logout error:', error)
    }
  }

  // 获取用户信息
  const getUserInfo = async () => {
    try {
      const response = await request.get('/api/auth/me')
      userInfo.value = response.data.data
      return { success: true }
    } catch (error) {
      logout()
      return { success: false }
    }
  }

  // 初始化
  const init = () => {
    if (token.value) {
      getUserInfo()
    }
  }

  return {
    token,
    userInfo,
    isLoggedIn,
    login,
    logout,
    getUserInfo,
    init
  }
})