export interface FlightOption {
  airline: string;
  flight_number: string;
  departure_time: string;
  arrival_time: string;
  origin: string;
  destination: string;
  price_inr: number;
  total_price_inr: number;
  duration: string;
  stops: number;
  is_demo: boolean;
}

export interface FlightSearchResult {
  origin: string;
  destination: string;
  travelers: number;
  total_options: number;
  options: FlightOption[];
  cheapest_option?: FlightOption;
  is_demo: boolean;
  note: string;
}

export interface HotelOption {
  hotel_name: string;
  rating: number;
  location: string;
  price_per_night_inr: number;
  total_price_inr: number;
  amenities: string[];
  room_type: string;
  is_demo: boolean;
}

export interface HotelSearchResult {
  destination: string;
  check_in?: string;
  check_out?: string;
  nights: number;
  total_options: number;
  options: HotelOption[];
  best_rated?: HotelOption;
  is_demo: boolean;
  note: string;
}

export interface WeatherForecastDay {
  date: string;
  temp_max_c: number;
  temp_min_c: number;
  precipitation_prob: number;
  weather_condition: string;
  icon_code: string;
}

export interface WeatherResult {
  destination: string;
  current_temp_c: number;
  weather_summary: string;
  forecast: WeatherForecastDay[];
  recommendations: string[];
}

export interface CostBreakdown {
  flights: number;
  accommodation: number;
  food: number;
  transport: number;
  activities: number;
  miscellaneous: number;
}

export interface BudgetAnalysis {
  estimated_total: number;
  budget_limit: number;
  remaining_budget: number;
  within_budget: boolean;
  cost_breakdown: CostBreakdown;
  recommendations: string[];
  status_label: string;
}

export interface ItineraryActivity {
  time_slot: string;
  activity_title: string;
  description: string;
  location: string;
  cost_inr: number;
}

export interface ItineraryDay {
  day_number: number;
  date?: string;
  theme: string;
  activities: ItineraryActivity[];
  daily_cost_inr: number;
}

export interface Itinerary {
  destination: string;
  total_days: number;
  days: ItineraryDay[];
  summary: string;
  highlights: string[];
}

export interface SupervisorDecision {
  destination: string;
  origin: string;
  travelers: number;
  duration_days: number;
  required_agents: string[];
  routing_reason: string;
  constraints: Record<string, any>;
}

export interface ToolCallInfo {
  agent_name: string;
  tool_name: string;
  arguments: Record<string, any>;
  result_summary: string;
  execution_time_ms: number;
  is_demo: boolean;
  timestamp: string;
}

export interface PlanResponse {
  session_id: string;
  request_id: string;
  status: 'completed' | 'waiting_for_approval' | 'blocked' | 'error';
  approval_status: 'pending' | 'approved' | 'edited' | 'rejected';
  supervisor_decision?: SupervisorDecision;
  selected_agents: string[];
  final_response?: string;
  tool_calls: ToolCallInfo[];
  is_demo: boolean;
}

export interface SessionDetail {
  session_id: string;
  request_id: string;
  user_query: string;
  destination?: string;
  origin?: string;
  approval_status: string;
  human_feedback?: string;
  final_response?: string;
  state?: Record<string, any>;
  created_at: string;
}
