export const metadata = {
  title: 'Contact Us - QuickToolsHub',
  description: 'Contact QuickToolsHub',
}

export default function Contact() {
  return (
    <div className="mx-auto max-w-4xl px-4 py-12 sm:px-6 lg:px-8">
      <h1 className="text-4xl font-bold mb-8">Contact Us</h1>
      
      <div className="prose prose-lg max-w-none">
        <section className="mb-8">
          <h2 className="text-2xl font-semibold mb-4">Get in Touch</h2>
          <p className="mb-4">
            We'd love to hear from you! Whether you have a question, suggestion, or feedback, 
            please don't hesitate to reach out to us.
          </p>
        </section>

        <section className="mb-8">
          <h2 className="text-2xl font-semibold mb-4">Email</h2>
          <p className="mb-4">
            For general inquiries, please email us at:
          </p>
          <p className="mb-4 text-blue-600">
            baifan7574@gmail.com
          </p>
        </section>

        <section className="mb-8">
          <h2 className="text-2xl font-semibold mb-4">Response Time</h2>
          <p className="mb-4">
            We aim to respond to all inquiries within 2-3 business days.
          </p>
        </section>

        <section className="mb-8">
          <h2 className="text-2xl font-semibold mb-4">Feedback</h2>
          <p className="mb-4">
            Your feedback helps us improve our tools and services. We appreciate your input!
          </p>
        </section>
      </div>
    </div>
  )
}

