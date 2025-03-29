# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 4.2.1-0-g80c4cb6)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class AppNotesDialog
###########################################################################

class AppNotesDialog ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Application Notes", pos = wx.DefaultPosition, size = wx.Size( 572,560 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

		self.SetSizeHints( wx.Size( 300,200 ), wx.Size( -1,-1 ) )

		fgSizer13 = wx.FlexGridSizer( 2, 1, 0, 0 )
		fgSizer13.AddGrowableCol( 0 )
		fgSizer13.AddGrowableRow( 0 )
		fgSizer13.SetFlexibleDirection( wx.BOTH )
		fgSizer13.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		gSizer1 = wx.GridSizer( 1, 1, 0, 0 )

		self.m_splitter2 = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.m_splitter2.Bind( wx.EVT_IDLE, self.m_splitter2OnIdle )

		self.m_splitter2.SetMinSize( wx.Size( 600,500 ) )

		self.m_scrolledWindow4 = wx.ScrolledWindow( self.m_splitter2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
		self.m_scrolledWindow4.SetScrollRate( 5, 5 )
		fgSizer5 = wx.FlexGridSizer( 2, 1, 0, 0 )
		fgSizer5.AddGrowableCol( 0 )
		fgSizer5.AddGrowableRow( 0 )
		fgSizer5.SetFlexibleDirection( wx.BOTH )
		fgSizer5.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.notesTree = wx.TreeCtrl( self.m_scrolledWindow4, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TR_DEFAULT_STYLE )
		self.notesTree.SetMinSize( wx.Size( 150,420 ) )

		fgSizer5.Add( self.notesTree, 0, wx.ALL|wx.EXPAND, 5 )


		self.m_scrolledWindow4.SetSizer( fgSizer5 )
		self.m_scrolledWindow4.Layout()
		fgSizer5.Fit( self.m_scrolledWindow4 )
		self.m_scrolledWindow2 = wx.ScrolledWindow( self.m_splitter2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
		self.m_scrolledWindow2.SetScrollRate( 5, 5 )
		self.webViewSizer = wx.BoxSizer( wx.VERTICAL )

		self.webViewSizer.SetMinSize( wx.Size( 400,400 ) )

		self.webViewSizer.Add( ( 0, 0), 1, wx.EXPAND, 5 )


		self.m_scrolledWindow2.SetSizer( self.webViewSizer )
		self.m_scrolledWindow2.Layout()
		self.webViewSizer.Fit( self.m_scrolledWindow2 )
		self.m_splitter2.SplitVertically( self.m_scrolledWindow4, self.m_scrolledWindow2, 164 )
		gSizer1.Add( self.m_splitter2, 1, wx.EXPAND, 5 )


		fgSizer13.Add( gSizer1, 1, wx.EXPAND, 5 )

		fgSizer4 = wx.FlexGridSizer( 1, 3, 0, 0 )
		fgSizer4.SetFlexibleDirection( wx.BOTH )
		fgSizer4.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_button21 = wx.Button( self, wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer4.Add( self.m_button21, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )


		fgSizer4.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_button2 = wx.Button( self, wx.ID_ANY, u"Insert", wx.DefaultPosition, wx.DefaultSize, 0 )

		self.m_button2.SetDefault()
		fgSizer4.Add( self.m_button2, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )


		fgSizer13.Add( fgSizer4, 1, wx.ALIGN_BOTTOM|wx.ALIGN_CENTER_HORIZONTAL, 5 )


		self.SetSizer( fgSizer13 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.notesTree.Bind( wx.EVT_TREE_ITEM_ACTIVATED, self.selectItem )
		self.notesTree.Bind( wx.EVT_TREE_SEL_CHANGED, self.selectItem )
		self.m_button21.Bind( wx.EVT_BUTTON, self.on_close )
		self.m_button2.Bind( wx.EVT_BUTTON, self.run )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def selectItem( self, event ):
		event.Skip()


	def on_close( self, event ):
		event.Skip()

	def run( self, event ):
		event.Skip()

	def m_splitter2OnIdle( self, event ):
		self.m_splitter2.SetSashPosition( 164 )
		self.m_splitter2.Unbind( wx.EVT_IDLE )


###########################################################################
## Class MyPanel4
###########################################################################

class MyPanel4 ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )


	def __del__( self ):
		pass


