import React from 'react';
import { motion } from 'framer-motion';
import { Github, Heart, Code, Zap } from 'lucide-react';

const Footer: React.FC = () => {
  return (
    <motion.footer
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5, delay: 0.8 }}
      className="mt-16 border-t border-dark-700/50"
    >
      <div className="container mx-auto px-4 py-8">
        <div className="grid md:grid-cols-3 gap-8">
          {/* Brand */}
          <div className="space-y-4">
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-primary-500 to-secondary-500 flex items-center justify-center">
                <Zap className="w-5 h-5 text-white" />
              </div>
              <div>
                <h3 className="text-lg font-bold gradient-text">Video Downloader Pro</h3>
                <p className="text-sm text-dark-400">React Edition</p>
              </div>
            </div>
            <p className="text-sm text-dark-400">
              A modern, fast, and reliable video downloader built with React, 
              featuring a beautiful dark theme and intuitive interface.
            </p>
          </div>

          {/* Features */}
          <div className="space-y-4">
            <h4 className="text-sm font-semibold text-dark-200">Features</h4>
            <ul className="space-y-2 text-sm text-dark-400">
              <li>• 1000+ supported sites</li>
              <li>• Multiple quality options</li>
              <li>• Real-time progress tracking</li>
              <li>• Modern dark theme</li>
              <li>• Responsive design</li>
              <li>• Fast downloads</li>
            </ul>
          </div>

          {/* Tech Stack */}
          <div className="space-y-4">
            <h4 className="text-sm font-semibold text-dark-200">Built With</h4>
            <div className="flex flex-wrap gap-2">
              {['React', 'TypeScript', 'Tailwind CSS', 'Framer Motion', 'React Query'].map((tech) => (
                <span
                  key={tech}
                  className="px-3 py-1 text-xs bg-dark-700 text-dark-300 rounded-full"
                >
                  {tech}
                </span>
              ))}
            </div>
          </div>
        </div>

        {/* Bottom */}
        <div className="mt-8 pt-6 border-t border-dark-700/50 flex flex-col md:flex-row items-center justify-between space-y-4 md:space-y-0">
          <div className="flex items-center space-x-2 text-sm text-dark-400">
            <span>Made with</span>
            <motion.div
              animate={{ scale: [1, 1.2, 1] }}
              transition={{ duration: 1, repeat: Infinity }}
            >
              <Heart className="w-4 h-4 text-red-400" />
            </motion.div>
            <span>using React & TypeScript</span>
          </div>
          
          <div className="flex items-center space-x-4">
            <motion.a
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              href="https://github.com"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center space-x-2 text-sm text-dark-400 hover:text-dark-200 transition-colors"
            >
              <Github className="w-4 h-4" />
              <span>GitHub</span>
            </motion.a>
            
            <motion.a
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              href="https://github.com"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center space-x-2 text-sm text-dark-400 hover:text-dark-200 transition-colors"
            >
              <Code className="w-4 h-4" />
              <span>Source</span>
            </motion.a>
          </div>
        </div>
      </div>
    </motion.footer>
  );
};

export default Footer;
