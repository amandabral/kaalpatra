export interface CalendarInfo {
    date: string;
    formatted_date: string;
    day_of_week: string;
    days_ago: number;
    moon_phase: string;
}

export interface LeadershipInfo {
    role: string;
    head_of_state: string;
    president: string;
}


export interface AnnualSnapshot {
  year: number;
  gold_price_10g: string | number;
  petrol_price_litre: string | number;
  usd_inr_rate: string | number;
  cinema_ticket_avg: string | number;
  typical_salary: string;
  era_badge: string;
  top_movie: string;
  top_song: string;
  lifestyle_summary: string;
}
export interface HistoricalEvent {
  id: number;
  date: string;
  title: string;
  description: string;
  category: string;
  category_display: string;
}
export interface Luminary {
  id: number;
  name: string;
  dob: string;
  field: string;
  field_display: string;
  bio: string;
}
export interface TimeCapsuleResponse {
  calendar: CalendarInfo;
  leadership: LeadershipInfo;
  annual_snapshot: AnnualSnapshot | null;
  exact_events: HistoricalEvent[];
  exact_twins: Luminary[];
  calendar_twins: Luminary[];
}