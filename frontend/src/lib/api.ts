import { TimeCapsuleResponse } from "@/types/capsule";

const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export async function getTimeCapsule(date: string): Promise<TimeCapsuleResponse> {
  const res = await fetch(`${BASE_URL}/capsule/?date=${date}`, {
    cache: "no-store",
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.error || `Failed to fetch capsule (${res.status})`);
  }

  return res.json();
}