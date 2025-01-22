import { createClient } from '@supabase/supabase-js'
import { WeatherData } from '@/types/weather'

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!

export const supabase = createClient(supabaseUrl, supabaseKey)

export async function fetchWeatherData(location: string): Promise<WeatherData[]> {
  const { data, error } = await supabase
    .from('weather_data')
    .select('*')
    .eq('location', location)
    .order('timestamp', { ascending: true })
  
  if (error) throw error
  return data as WeatherData[]
}