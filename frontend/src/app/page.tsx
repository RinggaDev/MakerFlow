import { redirect } from "next/navigation";

// ponytail: root just redirects to the real entry point — no logic needed here
export default function HomePage() {
  redirect("/plan");
}
