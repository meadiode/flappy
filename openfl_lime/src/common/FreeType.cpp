#include <Font.h>
#include <Utils.h>
#include <map>

#ifdef HX_WINRT
#define generic userGeneric
#endif

#include <ft2build.h>
#include FT_FREETYPE_H
#include FT_BITMAP_H
#include FT_SFNT_NAMES_H
#include FT_TRUETYPE_IDS_H

#ifdef ANDROID
#include <android/log.h>
#endif

#ifdef WEBOS
#include "PDL.h"
#endif

#ifndef HX_WINDOWS
#ifndef EPPC
#include <dirent.h>
#include <sys/stat.h>
#endif
#endif

#if defined(HX_WINDOWS) && !defined(HX_WINRT)
#define NOMINMAX
#include <windows.h>
#include <tchar.h>
#endif

#include "ByteArray.h"

#define LIME_FREETYPE_FLAGS  (FT_LOAD_FORCE_AUTOHINT|FT_LOAD_DEFAULT)

namespace lime
{

FT_Library sgLibrary = 0;


class FreeTypeFont : public FontFace
{
public:
   FreeTypeFont(FT_Face inFace, int inPixelHeight, int inTransform, void* inBuffer) :
     mFace(inFace), mPixelHeight(inPixelHeight),mTransform(inTransform), mBuffer(inBuffer)
   {
   }


   ~FreeTypeFont()
   {
      FT_Done_Face(mFace);
	  if (mBuffer) free(mBuffer);
   }

   bool LoadBitmap(int inChar)
   {
      int idx = FT_Get_Char_Index( mFace, inChar );
      int err = FT_Load_Glyph( mFace, idx, LIME_FREETYPE_FLAGS  );
      if (err)
         return false;

      FT_Render_Mode mode = FT_RENDER_MODE_NORMAL;
      // mode = FT_RENDER_MODE_MONO;
      if (mFace->glyph->format != FT_GLYPH_FORMAT_BITMAP)
         err = FT_Render_Glyph( mFace->glyph, mode );
      if (err)
         return false;

      #ifndef GPH
      if (mTransform & ffBold)
      {
         FT_GlyphSlot_Own_Bitmap(mFace->glyph);
         FT_Bitmap_Embolden(sgLibrary, &mFace->glyph->bitmap, 1<<6, 0);
      }
      #endif
      return true;
   }


   bool GetGlyphInfo(int inChar, int &outW, int &outH, int &outAdvance,
                           int &outOx, int &outOy)
   {
      if (!LoadBitmap(inChar))
         return false;

      outOx = mFace->glyph->bitmap_left;
      outOy = -mFace->glyph->bitmap_top;
      FT_Bitmap &bitmap = mFace->glyph->bitmap;
      outW = bitmap.width;
      outH = bitmap.rows;
      outAdvance = (mFace->glyph->advance.x);
      return true;
   }


   void RenderGlyph(int inChar,const RenderTarget &outTarget)
   {
      if (!LoadBitmap(inChar))
         return;

      FT_Bitmap &bitmap = mFace->glyph->bitmap;
      int w = bitmap.width;
      int h = bitmap.rows;
      if (w>outTarget.mRect.w || h>outTarget.mRect.h)
         return;

      for(int r=0;r<h;r++)
      {
         unsigned char *row = bitmap.buffer + r*bitmap.pitch;
         uint8  *dest = (uint8 *)outTarget.Row(r + outTarget.mRect.y) + outTarget.mRect.x;

         if (bitmap.pixel_mode == FT_PIXEL_MODE_MONO)
         {
            int bit = 0;
            int data = 0;
            for(int x=0;x<outTarget.mRect.w;x++)
            {
               if (!bit)
               {
                  bit = 128;
                  data = *row++;
               }
               *dest++ =  (data & bit) ? 0xff: 0x00;
               bit >>= 1;
            }
         }
         else if (bitmap.pixel_mode == FT_PIXEL_MODE_GRAY)
         {
            for(int x=0;x<w;x++)
               *dest ++ = *row++;
         }
      }
   }


   int Height()
   {
      return mFace->size->metrics.height/(1<<6);
   }


   void UpdateMetrics(TextLineMetrics &ioMetrics)
   {
      if (mFace)
      {
         FT_Size_Metrics &metrics = mFace->size->metrics;
         ioMetrics.ascent = std::max( ioMetrics.ascent, (float)metrics.ascender/(1<<6) );
         ioMetrics.descent = std::max( ioMetrics.descent, (float)fabs((float)metrics.descender/(1<<6)) );
         ioMetrics.height = std::max( ioMetrics.height, (float)metrics.height/(1<<6) );
      }
   }

   
   void* mBuffer;
   FT_Face  mFace;
   uint32 mTransform;
   int    mPixelHeight;

};

int MyNewFace(const std::string &inFace, int inIndex, FT_Face *outFace, QuickVec<unsigned char> *inBytes, void** outBuffer)
{
   *outFace = 0;
   *outBuffer = 0;
   int result = 0;
   result = FT_New_Face(sgLibrary, inFace.c_str(), inIndex, outFace);
   if (*outFace==0)
   {
     ByteArray bytes;
     if (inBytes == 0)
     {
         bytes = ByteArray::FromFile(inFace.c_str());
     }
     else
     {
         bytes = ByteArray(*inBytes);
     }
      if (bytes.Ok())
      {
         int l = bytes.Size();
         unsigned char *buf = (unsigned char*)malloc(l);
         memcpy(buf,bytes.Bytes(),l);
         result = FT_New_Memory_Face(sgLibrary, buf, l, inIndex, outFace);

         // The font owns the bytes here - so we just leak (fonts are not actually cleaned)
         if (!*outFace)
            free(buf);
         else *outBuffer = buf;
      }
   }
   return result;
}





static FT_Face OpenFont(const std::string &inFace, unsigned int inFlags, QuickVec<unsigned char> *inBytes, void** outBuffer)
{
   *outBuffer = 0;
   FT_Face face = 0;
   void* pBuffer = 0;
   MyNewFace(inFace.c_str(), 0, &face, inBytes, &pBuffer);
   if (face && inFlags!=0 && face->num_faces>1)
   {
      int n = face->num_faces;
      // Look for other font that may match
      for(int f=1;f<n;f++)
      {
         FT_Face test = 0;
         void* pTestBuffer = 0;
         MyNewFace(inFace.c_str(), f, &test, NULL, &pTestBuffer);
         if (test && test->style_flags == inFlags)
         {
            // A goodie!
            FT_Done_Face(face);
            if (pBuffer) free(pBuffer);
            *outBuffer = pTestBuffer;
            return test;
         }
         else if (test)
            FT_Done_Face(test);
      }
      // The original face will have to do...
   }
   *outBuffer = pBuffer;
   return face;
}





#ifdef HX_WINRT

bool GetFontFile(const std::string& inName,std::string &outFile)
{
   return false;
}

#elif defined(HX_WINDOWS)

#define strcasecmp stricmp

bool GetFontFile(const std::string& inName,std::string &outFile)
{
   
   std::string name = inName;
   
   if (!strcasecmp(inName.c_str(),"_serif")) {
      
      name = "georgia.ttf";
      
   } else if (!strcasecmp(inName.c_str(),"_sans")) {
      
      name = "arial.ttf";
      
   } else if (!strcasecmp(inName.c_str(),"_typewriter")) {
      
      name = "cour.ttf";
      
   }
   
   _TCHAR win_path[2 * MAX_PATH];
   GetWindowsDirectory(win_path, 2*MAX_PATH);
   outFile = std::string(win_path) + "\\Fonts\\" + name;

   return true;
}


#elif defined(GPH)

bool GetFontFile(const std::string& inName,std::string &outFile)
{
   outFile = "/usr/gp2x/HYUni_GPH_B.ttf";
   return true;
}

#elif defined(__APPLE__)
bool GetFontFile(const std::string& inName,std::string &outFile)
{

#ifdef IPHONEOS
#define FONT_BASE "/System/Library/Fonts/Cache/"
#else
#define FONT_BASE "/Library/Fonts/"
#endif
   
   outFile = FONT_BASE + inName;
   FILE *file = fopen(outFile.c_str(), "rb");
   if (file)
   {
      fclose(file);
      return true;
   }
   
   const char *serifFonts[] = { "Georgia.ttf", "Times.ttf", "Times New Roman.ttf", 0 };
   const char *sansFonts[] = { "Arial Unicode.ttf", "Arial.ttf", "Helvetica.ttf", 0 };
   const char *fixedFonts[] = { "Courier New.ttf", "Courier.ttf", 0 };
   
   const char **fontSet = 0;
   
   if (!strcasecmp(inName.c_str(),"_serif") || !strcasecmp(inName.c_str(),"times.ttf") || !strcasecmp(inName.c_str(),"times"))
      fontSet = serifFonts;
   else if (!strcasecmp(inName.c_str(),"_sans") || !strcasecmp(inName.c_str(),"helvetica.ttf"))
      fontSet = sansFonts;
   else if (!strcasecmp(inName.c_str(),"_typewriter") || !strcasecmp(inName.c_str(),"courier.ttf"))
      fontSet = fixedFonts;
   else if (!strcasecmp(inName.c_str(),"arial.ttf"))
      fontSet = sansFonts;
   
   if (fontSet)
   {
      while (*fontSet)
      {
         outFile = FONT_BASE + std::string(*fontSet);
         
         FILE *file = fopen(outFile.c_str(), "rb");
         if (file)
         {
            fclose(file);
            return true;
         }
         fontSet++;
      }
   }

   return false;
}
#else

bool GetFontFile(const std::string& inName,std::string &outFile)
{
   if (!strcasecmp(inName.c_str(),"_serif") || !strcasecmp(inName.c_str(),"times.ttf") || !strcasecmp(inName.c_str(),"times")) {
      
      #if defined (ANDROID)
         outFile = "/system/fonts/DroidSerif-Regular.ttf";
      #elif defined (WEBOS)
         outFile = "/usr/share/fonts/times.ttf";
      #elif defined (BLACKBERRY)
         outFile = "/usr/fonts/font_repository/monotype/times.ttf";
      #elif defined (TIZEN)
         outFile = "/usr/share/fonts/TizenSansRegular.ttf";
      #else
         outFile = "/usr/share/fonts/truetype/freefont/FreeSerif.ttf";
      #endif
      
   } else if (!strcasecmp(inName.c_str(),"_sans") || !strcasecmp(inName.c_str(),"arial.ttf") || !strcasecmp(inName.c_str(),"arial")) {
      
      #if defined (ANDROID)
         outFile = "/system/fonts/DroidSans.ttf";
      #elif defined (WEBOS)
         outFile = "/usr/share/fonts/Prelude-Medium.ttf";
      #elif defined (BLACKBERRY)
         outFile = "/usr/fonts/font_repository/monotype/arial.ttf";
      #elif defined (TIZEN)
         outFile = "/usr/share/fonts/TizenSansRegular.ttf";
      #else
         outFile = "/usr/share/fonts/truetype/freefont/FreeSans.ttf";
      #endif
      
   } else if (!strcasecmp(inName.c_str(),"_typewriter") || !strcasecmp(inName.c_str(),"courier.ttf") || !strcasecmp(inName.c_str(),"courier")) {
      
      #if defined (ANDROID)
         outFile = "/system/fonts/DroidSansMono.ttf";
      #elif defined (WEBOS)
         outFile = "/usr/share/fonts/cour.ttf";
      #elif defined (BLACKBERRY)
         outFile = "/usr/fonts/font_repository/monotype/cour.ttf";
      #elif defined (TIZEN)
         outFile = "/usr/share/fonts/TizenSansRegular.ttf";
      #else
         outFile = "/usr/share/fonts/truetype/freefont/FreeMono.ttf";
      #endif
      
   } else {
      
      #ifdef ANDROID
       __android_log_print(ANDROID_LOG_INFO, "GetFontFile1", "Could not load font %s.",
          inName.c_str() );
       #endif
      
      //printf("Unfound font: %s\n",inName.c_str());
      return false;
      
   }

   return true;
}
#endif


std::string ToAssetName(const std::string &inPath)
{
#if HX_MACOS
   std::string flat;
   for(int i=0;i<inPath.size();i++)
   {
      int ch = inPath[i];
      if ( (ch>='a' && ch<='z') || (ch>='0' && ch<='9') )
         { }
      else if (ch>='A' && ch<='Z')
         ch += 'a' - 'A';
      else
         ch = '_';

      flat.push_back(ch);
   }

   char name[1024];
   GetBundleFilename(flat.c_str(),name,1024);
   return name;
#else
   return gAssetBase + "/" + inPath;
#endif
}

FT_Face FindFont(const std::string &inFontName, unsigned int inFlags, QuickVec<unsigned char> *inBytes, void** pBuffer)
{
   std::string fname = inFontName;
   
   #ifndef ANDROID
   if (fname.find(".") == std::string::npos && fname.find("_") == std::string::npos)
      fname += ".ttf";
   #endif
     
   FT_Face font = OpenFont(fname,inFlags,inBytes, pBuffer);

   if (font==0 && fname.find("\\")==std::string::npos && fname.find("/")==std::string::npos)
   {
      std::string file_name;

      #if HX_MACOS
      font = OpenFont(ToAssetName(fname).c_str(),inFlags,NULL,pBuffer);
      #endif

      if (font==0 && GetFontFile(fname,file_name))
      {
         // printf("Found font in %s\n", file_name.c_str());
         font = OpenFont(file_name.c_str(),inFlags,NULL,pBuffer);

         // printf("Opened : %p\n", font);
      }
   }


   return font;
}




FontFace *FontFace::CreateFreeType(const TextFormat &inFormat,double inScale, QuickVec<unsigned char> *inBytes)
{
   if (!sgLibrary)
     FT_Init_FreeType( &sgLibrary );
   if (!sgLibrary)
      return 0;

   FT_Face face = 0;
   std::string str = WideToUTF8(inFormat.font);

   uint32 flags = 0;
   if (inFormat.bold)
      flags |= ffBold;
   if (inFormat.italic)
      flags |= ffItalic;
   
   void* pBuffer = 0;
   face = FindFont(str,flags,inBytes,&pBuffer);
   if (!face)
      return 0;

   int height = (int )(inFormat.size*inScale + 0.5);
   FT_Set_Pixel_Sizes(face,0, height);


   uint32 transform = 0;
   if ( !(face->style_flags & ffBold) && inFormat.bold )
      transform |= ffBold;
   if ( !(face->style_flags & ffItalic) && inFormat.italic )
      transform |= ffItalic;
   return new FreeTypeFont(face,height,transform,pBuffer);
}





} // end namespace lime

