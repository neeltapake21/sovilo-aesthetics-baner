import { Link } from "react-router-dom";

export function FinalCta() {
  return (
    <section className="mt-16 bg-gradient-to-r from-primary to-primary-light py-16 text-white">
      <div className="container-xl text-center">
        <h2 className="font-heading text-3xl font-bold">Ready to Transform Your Life?</h2>
        <p className="mt-3 text-sm md:text-base">
          Book your consultation today and take the first step towards a more confident you.
        </p>
        <Link
          to="/contact"
          className="mt-8 inline-flex items-center justify-center rounded-full bg-white px-10 py-3 text-base font-semibold text-primary shadow-lg transition-transform hover:scale-105"
        >
          Book Consultation
        </Link>
      </div>
    </section>
  );
}

