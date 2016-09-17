from PIL import Image

from minfo import app_dir

cmp_im = Image.open('%s/cls/%s.jpg' % (app_dir,))
cmp_im.save('%s/cls/%s.jpg' % (app_dir,self.t,), optimize=True, quality=80)
