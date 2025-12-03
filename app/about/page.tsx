export const metadata = {
  title: 'About Us - QuickToolsHub',
  description: 'About QuickToolsHub - Free online tools',
}

export default function About() {
  return (
    <div className="mx-auto max-w-4xl px-4 py-12 sm:px-6 lg:px-8">
      <h1 className="text-4xl font-bold mb-8">About Us</h1>
      
      <div className="prose prose-lg max-w-none">
        <section className="mb-8">
          <h2 className="text-2xl font-semibold mb-4">Our Mission</h2>
          <p className="mb-4">
            QuickToolsHub is dedicated to providing free, high-quality online tools that help users 
            accomplish their tasks quickly and efficiently. We believe that everyone should have access 
            to powerful tools without barriers.
          </p>
        </section>

        <section className="mb-8">
          <h2 className="text-2xl font-semibold mb-4">What We Offer</h2>
          <p className="mb-4">
            We offer a wide range of free online tools including:
          </p>
          <ul className="list-disc pl-6 mb-4">
            <li>PDF tools for merging, splitting, and converting</li>
            <li>Image tools for compression, conversion, and editing</li>
            <li>Text tools for counting, formatting, and processing</li>
            <li>Developer tools for coding and testing</li>
            <li>And many more useful tools</li>
          </ul>
        </section>

        <section className="mb-8">
          <h2 className="text-2xl font-semibold mb-4">Our Values</h2>
          <ul className="list-disc pl-6 mb-4">
            <li><strong>Free Access:</strong> All our tools are free to use</li>
            <li><strong>No Registration:</strong> Use our tools without creating an account</li>
            <li><strong>Privacy First:</strong> We respect your privacy and data</li>
            <li><strong>Quality Tools:</strong> We provide reliable and efficient tools</li>
          </ul>
        </section>

        <section className="mb-8">
          <h2 className="text-2xl font-semibold mb-4">Contact Us</h2>
          <p className="mb-4">
            If you have any questions, suggestions, or feedback, please contact us at:
          </p>
          <p className="mb-4">
            Email: baifan7574@gmail.com
          </p>
        </section>
      </div>
    </div>
  )
}

