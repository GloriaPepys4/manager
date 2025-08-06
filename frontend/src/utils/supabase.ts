import { createClient } from '@supabase/supabase-js'

const supabaseUrl = 'https://ohjygwqwsckdcrfwawtp.supabase.co'
const supabaseAnonKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9oanlnd3F3c2NrZGNyZndhd3RwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ0NjI1NjcsImV4cCI6MjA3MDAzODU2N30.UrmGwFIbICNfxT9-D1AdHUi9bdM11Z_Zewa-HEd6EeM'

export const supabase = createClient(supabaseUrl, supabaseAnonKey)

// 数据库表类型定义
export interface Database {
  public: {
    Tables: {
      users: {
        Row: {
          id: string
          username: string
          email: string
          password_hash: string
          role: string
          created_at: string
          updated_at: string
        }
        Insert: {
          id?: string
          username: string
          email: string
          password_hash: string
          role?: string
          created_at?: string
          updated_at?: string
        }
        Update: {
          id?: string
          username?: string
          email?: string
          password_hash?: string
          role?: string
          created_at?: string
          updated_at?: string
        }
      }
      fleets: {
        Row: {
          id: string
          name: string
          contact_person: string | null
          phone: string | null
          address: string | null
          status: string
          created_at: string
          updated_at: string
        }
        Insert: {
          id?: string
          name: string
          contact_person?: string | null
          phone?: string | null
          address?: string | null
          status?: string
          created_at?: string
          updated_at?: string
        }
        Update: {
          id?: string
          name?: string
          contact_person?: string | null
          phone?: string | null
          address?: string | null
          status?: string
          created_at?: string
          updated_at?: string
        }
      }
      vehicles: {
        Row: {
          id: string
          license_plate: string
          fleet_id: string | null
          vehicle_type: string | null
          driver_name: string | null
          driver_phone: string | null
          status: string
          remark: string | null
          created_at: string
          updated_at: string
        }
        Insert: {
          id?: string
          license_plate: string
          fleet_id?: string | null
          vehicle_type?: string | null
          driver_name?: string | null
          driver_phone?: string | null
          status?: string
          remark?: string | null
          created_at?: string
          updated_at?: string
        }
        Update: {
          id?: string
          license_plate?: string
          fleet_id?: string | null
          vehicle_type?: string | null
          driver_name?: string | null
          driver_phone?: string | null
          status?: string
          remark?: string | null
          created_at?: string
          updated_at?: string
        }
      }
    }
  }
}