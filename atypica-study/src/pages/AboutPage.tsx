export default function AboutPage() {
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-6">About Atypica Study</h1>
      
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-8">
        <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">Our Mission</h2>
        <p className="text-gray-600 dark:text-gray-300 mb-4">
          Atypica Study is a platform dedicated to advancing AI research through collaborative studies and experiments.
          We believe in the power of human-AI interaction to create more helpful, safe, and effective AI systems.
        </p>
        <p className="text-gray-600 dark:text-gray-300">
          Our mission is to facilitate meaningful research that improves AI capabilities while ensuring these systems
          are aligned with human values and needs.
        </p>
      </div>
      
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-8">
        <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">How It Works</h2>
        <div className="space-y-4">
          <div className="flex">
            <div className="flex-shrink-0">
              <div className="flex items-center justify-center h-12 w-12 rounded-md bg-primary-500 text-white">
                <span className="text-xl font-bold">1</span>
              </div>
            </div>
            <div className="ml-4">
              <h3 className="text-lg font-medium text-gray-900 dark:text-white">Browse Studies</h3>
              <p className="mt-1 text-gray-600 dark:text-gray-300">
                Explore our collection of AI research studies covering various topics and capabilities.
              </p>
            </div>
          </div>
          
          <div className="flex">
            <div className="flex-shrink-0">
              <div className="flex items-center justify-center h-12 w-12 rounded-md bg-primary-500 text-white">
                <span className="text-xl font-bold">2</span>
              </div>
            </div>
            <div className="ml-4">
              <h3 className="text-lg font-medium text-gray-900 dark:text-white">Participate</h3>
              <p className="mt-1 text-gray-600 dark:text-gray-300">
                Join studies that interest you and interact with AI agents designed for specific research purposes.
              </p>
            </div>
          </div>
          
          <div className="flex">
            <div className="flex-shrink-0">
              <div className="flex items-center justify-center h-12 w-12 rounded-md bg-primary-500 text-white">
                <span className="text-xl font-bold">3</span>
              </div>
            </div>
            <div className="ml-4">
              <h3 className="text-lg font-medium text-gray-900 dark:text-white">Provide Feedback</h3>
              <p className="mt-1 text-gray-600 dark:text-gray-300">
                Share your experience and insights to help improve AI systems and contribute to research.
              </p>
            </div>
          </div>
        </div>
      </div>
      
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
        <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">Privacy & Ethics</h2>
        <p className="text-gray-600 dark:text-gray-300 mb-4">
          We are committed to conducting research ethically and responsibly. All studies undergo review to ensure they
          meet our standards for participant safety and data privacy.
        </p>
        <p className="text-gray-600 dark:text-gray-300 mb-4">
          Your participation in studies is voluntary, and you can withdraw at any time. We collect and use data in
          accordance with our privacy policy, which you can review before joining any study.
        </p>
        <p className="text-gray-600 dark:text-gray-300">
          If you have questions or concerns about our research practices, please contact our ethics team at
          <a href="mailto:ethics@atypica.ai" className="text-primary-600 hover:text-primary-800 ml-1">ethics@atypica.ai</a>.
        </p>
      </div>
    </div>
  );
}