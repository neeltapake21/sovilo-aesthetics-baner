import { Hero } from "../sections/home/Hero";
import { DoctorProfile } from "../sections/home/DoctorProfile";
import { ServicesOverview } from "../sections/home/ServicesOverview";
import { Reviews } from "../sections/home/Reviews";
import { FinalCta } from "../sections/home/FinalCta";


export function Home() {
  return (
    <div>
      <Hero />
      <DoctorProfile />
      <ServicesOverview />
      <Reviews />
      <FinalCta />
    </div>
  );
}

