# Cell 2: RUN THE SERVER
import asyncio
import os
from google.colab import output

# Change to app directory
os.chdir('/content/simple')

# Import the app
from app import app

# Enable Colab port forwarding
output.serve_kernel_port_as_window(8000)

print('='*70)
print('🚀 THREE.JS VISUALIZATION SERVER (Tier 2 Enhanced)')
print('='*70)
print('✅ Server running on port 8000')
print('📊 Visualization opening in new window...')
print('')
print('🔧 Features Enabled:')
print('  ✅ WebGL error detection')
print('  ✅ "Open in New Tab" fallback')
print('  ✅ Performance monitoring')
print('  ✅ Enhanced error messages')
print('')
print('💡 If you see a black screen:')
print('  1. Click "Open in New Tab" button (top right)')
print('  2. Check browser console for details (F12)')
print('  3. Enable hardware acceleration in browser')
print('')
print('🔗 Endpoints:')
print('   - Main: /')
print('   - API: /api/data')
print('='*70)
print('\n🛑 To stop: Runtime > Interrupt execution')
print()

# Run server
await app.run_task(host='0.0.0.0', port=8000, debug=False)
