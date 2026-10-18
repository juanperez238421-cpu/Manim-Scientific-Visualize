import { Nav, Hero, How, Gallery, Plans, Faq, Cta, Footer } from "@/components/Landing";

export default function Home() {
  return (
    <>
      <Nav />
      <main id="main"><Hero /><How /><Gallery /><Plans /><Faq /><Cta /></main>
      <Footer />
    </>
  );
}
