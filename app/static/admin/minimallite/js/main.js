/**
 * Created by xuannan on 2019-02-09.
 */
//[Master Javascript]

//Project:	MinimalLite Admin - Responsive Admin Template
//Primary use:	MinimalLite Admin - Responsive Admin Template

//should be included in all pages. It controls some layout

$(function () {
    $(".preloader").fadeOut();
}), jQuery(document).on("click", ".mega-dropdown", function (i) {
    i.stopPropagation();
})
//初始化select2
$('.select2').select2({
    language: "zh-CN",
    minimumInputLength: 0,
    placeholder: "请选择",//默认值
    allowClear: true,
})
$('.select2').change(function () {
    var arr = [];
    $(this).select2('data').forEach(function (v) {
        arr.push(v.id)
    });
    $(this).prev().val(arr.join(','))
})
//初始化tooltip
$('[data-toggle="tooltip"]').tooltip()


$('.treeview-menu').find('li').each(function () {
    if ($(this).hasClass('active')) {
        $(this).parent().parent().addClass('menu-open active')
    }
})
// Make sure jQuery has been loaded
if (typeof jQuery === 'undefined') {
    throw new Error('template requires jQuery')
}

// Layout()

//  Implements layout.
//  Fixes the layout height in case min-height fails.

//  @usage activated automatically upon window load.
//  Configure any options by passing data-option="value"
//  to the body tag.


+function ($) {
    'use strict'

    var DataKey = 'aries.layout'

    var Default = {
        slimscroll: true,
        resetHeight: true
    }

    var Selector = {
        wrapper: '.wrapper',
        contentWrapper: '.content-wrapper',
        layoutBoxed: '.layout-boxed',
        mainFooter: '.main-footer',
        mainHeader: '.main-header',
        sidebar: '.sidebar',
        controlSidebar: '.control-sidebar',
        fixed: '.fixed',
        sidebarMenu: '.sidebar-menu',
        logo: '.main-header .logo'
    }

    var ClassName = {
        fixed: 'fixed',
        holdTransition: 'hold-transition'
    }

    var Layout = function (options) {
        this.options = options
        this.bindedResize = false
        this.activate()
    }

    Layout.prototype.activate = function () {
        this.fix()
        this.fixSidebar()

        $('body').removeClass(ClassName.holdTransition)

        if (this.options.resetHeight) {
            $('body, html, ' + Selector.wrapper).css({
                'height': 'auto',
                'min-height': '100%'
            })
        }

        if (!this.bindedResize) {
            $(window).resize(function () {
                this.fix()
                this.fixSidebar()

                $(Selector.logo + ', ' + Selector.sidebar).one('webkitTransitionEnd otransitionend oTransitionEnd msTransitionEnd transitionend', function () {
                    this.fix()
                    this.fixSidebar()
                }.bind(this))
            }.bind(this))

            this.bindedResize = true
        }

        $(Selector.sidebarMenu).on('expanded.tree', function () {
            this.fix()
            this.fixSidebar()
        }.bind(this))

        $(Selector.sidebarMenu).on('collapsed.tree', function () {
            this.fix()
            this.fixSidebar()
        }.bind(this))
    }

    Layout.prototype.fix = function () {
        // Remove overflow from .wrapper if layout-boxed exists
        $(Selector.layoutBoxed + ' > ' + Selector.wrapper).css('overflow', 'hidden')

        // Get window height and the wrapper height
        var footerHeight = $(Selector.mainFooter).outerHeight() || 0
        var neg = $(Selector.mainHeader).outerHeight() + footerHeight
        var windowHeight = $(window).height()
        var sidebarHeight = $(Selector.sidebar).height() || 0

        // Set the min-height of the content and sidebar based on
        // the height of the document.
        if ($('body').hasClass(ClassName.fixed)) {
            $(Selector.contentWrapper).css('min-height', windowHeight - footerHeight)
        } else {
            var postSetHeight

            if (windowHeight >= sidebarHeight) {
                $(Selector.contentWrapper).css('min-height', windowHeight - neg)
                postSetHeight = windowHeight - neg
            } else {
                $(Selector.contentWrapper).css('min-height', sidebarHeight)
                postSetHeight = sidebarHeight
            }

            // Fix for the control sidebar height
            var $controlSidebar = $(Selector.controlSidebar)
            if (typeof $controlSidebar !== 'undefined') {
                if ($controlSidebar.height() > postSetHeight)
                    $(Selector.contentWrapper).css('min-height', $controlSidebar.height())
            }
        }
    }

    Layout.prototype.fixSidebar = function () {
        // Make sure the body tag has the .fixed class
        if (!$('body').hasClass(ClassName.fixed)) {
            if (typeof $.fn.slimScroll !== 'undefined') {
                $(Selector.sidebar).slimScroll({destroy: true}).height('auto')
            }
            return
        }

        // Enable slimscroll for fixed layout
        if (this.options.slimscroll) {
            if (typeof $.fn.slimScroll !== 'undefined') {
                // Destroy if it exists
                $(Selector.sidebar).slimScroll({destroy: true}).height('auto')

                // Add slimscroll
                $(Selector.sidebar).slimScroll({
                    height: ($(window).height() - $(Selector.mainHeader).height()) + 'px',
                    color: 'rgba(0,0,0,0.2)',
                    size: '3px'
                })
            }
        }
    }

    // Plugin Definition
    function Plugin(option) {
        return this.each(function () {
            var $this = $(this)
            var data = $this.data(DataKey)

            if (!data) {
                var options = $.extend({}, Default, $this.data(), typeof option === 'object' && option)
                $this.data(DataKey, (data = new Layout(options)))
            }

            if (typeof option == 'string') {
                if (typeof data[option] == 'undefined') {
                    throw new Error('No method named ' + option)
                }
                data[option]()
            }
        })
    }

    var old = $.fn.layout

    $.fn.layout = Plugin
    $.fn.layout.Constuctor = Layout

    // No conflict mode
    $.fn.layout.noConflict = function () {
        $.fn.layout = old
        return this
    }

    // Layout DATA-API
    $(window).on('load', function () {
        Plugin.call($('body'))
    });
}(jQuery)  // End of use strict

    /* PushMenu()
     * Adds the push menu functionality to the sidebar.
     *
     * @usage: $('.btn').pushMenu(options)
     *          or add [data-toggle="push-menu"] to any button
     *          Pass any option as data-option="value"
     */
+ function ($) {
    'use strict'

    var DataKey = 'aries.pushmenu'

    var Default = {
        collapseScreenSize: 767,
        expandOnHover: false,
        expandTransitionDelay: 200
    }

    var Selector = {
        collapsed: '.sidebar-collapse',
        open: '.sidebar-open',
        mainSidebar: '.main-sidebar',
        contentWrapper: '.content-wrapper',
        searchInput: '.sidebar-form .form-control',
        button: '[data-toggle="push-menu"]',
        mini: '.sidebar-mini',
        expanded: '.sidebar-expanded-on-hover',
        layoutFixed: '.fixed'
    }

    var ClassName = {
        collapsed: 'sidebar-collapse',
        open: 'sidebar-open',
        mini: 'sidebar-mini',
        expanded: 'sidebar-expanded-on-hover',
        expandFeature: 'sidebar-mini-expand-feature',
        layoutFixed: 'fixed'
    }

    var Event = {
        expanded: 'expanded.pushMenu',
        collapsed: 'collapsed.pushMenu'
    }

    // PushMenu Class Definition
    var PushMenu = function (options) {
        this.options = options
        this.init()
    }

    PushMenu.prototype.init = function () {
        if (this.options.expandOnHover
            || ($('body').is(Selector.mini + Selector.layoutFixed))) {
            this.expandOnHover()
            $('body').addClass(ClassName.expandFeature)
        }

        $(Selector.contentWrapper).on(function () {
            // Enable hide menu when clicking on the content-wrapper on small screens
            if ($(window).width() <= this.options.collapseScreenSize && $('body').hasClass(ClassName.open)) {
                this.close()
            }
        }.bind(this))

        // __Fix for android devices
        $(Selector.searchInput).on(function (e) {
            e.stopPropagation()
        })
    }

    PushMenu.prototype.toggle = function () {
        var windowWidth = $(window).width()
        var isOpen = !$('body').hasClass(ClassName.collapsed)

        if (windowWidth <= this.options.collapseScreenSize) {
            isOpen = $('body').hasClass(ClassName.open)
        }

        if (!isOpen) {
            this.open()
        } else {
            this.close()
        }
    }

    PushMenu.prototype.open = function () {
        var windowWidth = $(window).width()

        if (windowWidth > this.options.collapseScreenSize) {
            $('body').removeClass(ClassName.collapsed)
                .trigger($.Event(Event.expanded))
        }
        else {
            $('body').addClass(ClassName.open)
                .trigger($.Event(Event.expanded))
        }
    }

    PushMenu.prototype.close = function () {
        var windowWidth = $(window).width()
        if (windowWidth > this.options.collapseScreenSize) {
            $('body').addClass(ClassName.collapsed)
                .trigger($.Event(Event.collapsed))
        } else {
            $('body').removeClass(ClassName.open + ' ' + ClassName.collapsed)
                .trigger($.Event(Event.collapsed))
        }
    }

    PushMenu.prototype.expandOnHover = function () {
        $(Selector.mainSidebar).hover(function () {
            if ($('body').is(Selector.mini + Selector.collapsed)
                && $(window).width() > this.options.collapseScreenSize) {
                this.expand()
            }
        }.bind(this), function () {
            if ($('body').is(Selector.expanded)) {
                this.collapse()
            }
        }.bind(this))
    }

    PushMenu.prototype.expand = function () {
        setTimeout(function () {
            $('body').removeClass(ClassName.collapsed)
                .addClass(ClassName.expanded)
        }, this.options.expandTransitionDelay)
    }

    PushMenu.prototype.collapse = function () {
        setTimeout(function () {
            $('body').removeClass(ClassName.expanded)
                .addClass(ClassName.collapsed)
        }, this.options.expandTransitionDelay)
    }

    // PushMenu Plugin Definition
    function Plugin(option) {
        return this.each(function () {
            var $this = $(this)
            var data = $this.data(DataKey)

            if (!data) {
                var options = $.extend({}, Default, $this.data(), typeof option === 'object' && option)
                $this.data(DataKey, (data = new PushMenu(options)))
            }

            if (option == 'toggle') data.toggle()
        })
    }

    var old = $.fn.pushMenu

    $.fn.pushMenu = Plugin
    $.fn.pushMenu.Constructor = PushMenu

    // No Conflict Mode
    $.fn.pushMenu.noConflict = function () {
        $.fn.pushMenu = old
        return this
    }

    // Data API
    $(document).on('click', Selector.button, function (e) {
        e.preventDefault()
        Plugin.call($(this), 'toggle')
    })
    $(window).on('load', function () {
        Plugin.call($(Selector.button))
    })
}(jQuery) // End of use strict


    /* Tree()
     * Converts a nested list into a multilevel
     * tree view menu.
     *
     * @Usage: $('.my-menu').tree(options)
     *         or add [data-widget="tree"] to the ul element
     *         Pass any option as data-option="value"
     */
+ function ($) {
    'use strict'

    var DataKey = 'aries.tree'

    var Default = {
        animationSpeed: 500,
        accordion: true,
        followLink: false,
        trigger: '.treeview a'
    }

    var Selector = {
        tree: '.tree',
        treeview: '.treeview',
        treeviewMenu: '.treeview-menu',
        open: '.menu-open, .active',
        li: 'li',
        data: '[data-widget="tree"]',
        active: '.active'
    }

    var ClassName = {
        open: 'menu-open',
        tree: 'tree'
    }

    var Event = {
        collapsed: 'collapsed.tree',
        expanded: 'expanded.tree'
    }

    // Tree Class Definition
    var Tree = function (element, options) {
        this.element = element
        this.options = options

        $(this.element).addClass(ClassName.tree)

        $(Selector.treeview + Selector.active, this.element).addClass(ClassName.open)

        this._setUpListeners()
    }

    Tree.prototype.toggle = function (link, event) {
        var treeviewMenu = link.next(Selector.treeviewMenu)
        var parentLi = link.parent()
        var isOpen = parentLi.hasClass(ClassName.open)

        if (!parentLi.is(Selector.treeview)) {
            return
        }

        if (!this.options.followLink || link.attr('href') == '#') {
            event.preventDefault()
        }

        if (isOpen) {
            this.collapse(treeviewMenu, parentLi)
        } else {
            this.expand(treeviewMenu, parentLi)
        }
    }

    Tree.prototype.expand = function (tree, parent) {
        var expandedEvent = $.Event(Event.expanded)

        if (this.options.accordion) {
            var openMenuLi = parent.siblings(Selector.open)
            var openTree = openMenuLi.children(Selector.treeviewMenu)
            this.collapse(openTree, openMenuLi)
        }

        parent.addClass(ClassName.open)
        tree.slideDown(this.options.animationSpeed, function () {
            $(this.element).trigger(expandedEvent)
        }.bind(this))
    }

    Tree.prototype.collapse = function (tree, parentLi) {
        var collapsedEvent = $.Event(Event.collapsed)

        tree.find(Selector.open).removeClass(ClassName.open)
        parentLi.removeClass(ClassName.open)
        tree.slideUp(this.options.animationSpeed, function () {
            tree.find(Selector.open + ' > ' + Selector.treeview).slideUp()
            $(this.element).trigger(collapsedEvent)
        }.bind(this))
    }

    // Private

    Tree.prototype._setUpListeners = function () {
        var that = this

        $(this.element).on('click', this.options.trigger, function (event) {
            that.toggle($(this), event)
        })
    }

    // Plugin Definition
    function Plugin(option) {
        return this.each(function () {
            var $this = $(this)
            var data = $this.data(DataKey)

            if (!data) {
                var options = $.extend({}, Default, $this.data(), typeof option === 'object' && option)
                $this.data(DataKey, new Tree($this, options))
            }
        })
    }

    var old = $.fn.tree

    $.fn.tree = Plugin
    $.fn.tree.Constructor = Tree

    // No Conflict Mode
    $.fn.tree.noConflict = function () {
        $.fn.tree = old
        return this
    }

    // Tree Data API
    $(window).on('load', function () {
        $(Selector.data).each(function () {
            Plugin.call($(this))
        })
    })

}(jQuery) // End of use strict


    /* ControlSidebar()
     * Toggles the state of the control sidebar
     *
     * @Usage: $('#control-sidebar-trigger').controlSidebar(options)
     *         or add [data-toggle="control-sidebar"] to the trigger
     *         Pass any option as data-option="value"
     */
+ function ($) {
    'use strict'

    var DataKey = 'aries.controlsidebar'

    var Default = {
        slide: true
    }

    var Selector = {
        sidebar: '.control-sidebar',
        data: '[data-toggle="control-sidebar"]',
        open: '.control-sidebar-open',
        bg: '.control-sidebar-bg',
        wrapper: '.wrapper',
        content: '.content-wrapper',
        boxed: '.layout-boxed'
    }

    var ClassName = {
        open: 'control-sidebar-open',
        fixed: 'fixed'
    }

    var Event = {
        collapsed: 'collapsed.controlsidebar',
        expanded: 'expanded.controlsidebar'
    }

    // ControlSidebar Class Definition
    var ControlSidebar = function (element, options) {
        this.element = element
        this.options = options
        this.hasBindedResize = false

        this.init()
    }

    ControlSidebar.prototype.init = function () {
        // Add click listener if the element hasn't been
        // initialized using the data API
        if (!$(this.element).is(Selector.data)) {
            $(this).on('click', this.toggle)
        }

        this.fix()
        $(window).resize(function () {
            this.fix()
        }.bind(this))
    }

    ControlSidebar.prototype.toggle = function (event) {
        if (event) event.preventDefault()

        this.fix()

        if (!$(Selector.sidebar).is(Selector.open) && !$('body').is(Selector.open)) {
            this.expand()
        } else {
            this.collapse()
        }
    }

    ControlSidebar.prototype.expand = function () {
        if (!this.options.slide) {
            $('body').addClass(ClassName.open)
        } else {
            $(Selector.sidebar).addClass(ClassName.open)
        }

        $(this.element).trigger($.Event(Event.expanded))
    }

    ControlSidebar.prototype.collapse = function () {
        $('body, ' + Selector.sidebar).removeClass(ClassName.open)
        $(this.element).trigger($.Event(Event.collapsed))
    }

    ControlSidebar.prototype.fix = function () {
        if ($('body').is(Selector.boxed)) {
            this._fixForBoxed($(Selector.bg))
        }
    }

    // Private

    ControlSidebar.prototype._fixForBoxed = function (bg) {
        bg.css({
            position: 'absolute',
            height: $(Selector.wrapper).height()
        })
    }

    // Plugin Definition
    function Plugin(option) {
        return this.each(function () {
            var $this = $(this)
            var data = $this.data(DataKey)

            if (!data) {
                var options = $.extend({}, Default, $this.data(), typeof option === 'object' && option)
                $this.data(DataKey, (data = new ControlSidebar($this, options)))
            }

            if (typeof option == 'string') data.toggle()
        })
    }

    var old = $.fn.controlSidebar

    $.fn.controlSidebar = Plugin
    $.fn.controlSidebar.Constructor = ControlSidebar

    // No Conflict Mode
    $.fn.controlSidebar.noConflict = function () {
        $.fn.controlSidebar = old
        return this
    }

    // ControlSidebar Data API
    $(document).on('click', Selector.data, function (event) {
        if (event) event.preventDefault()
        Plugin.call($(this), 'toggle')
    })

}(jQuery) // End of use strict


    /* BoxWidget()
     * Adds box widget functions to boxes.
     *
     * @Usage: $('.my-box').boxWidget(options)
     *         This plugin auto activates on any element using the `.box` class
     *         Pass any option as data-option="value"
     */
+ function ($) {
    'use strict'

    var DataKey = 'aries.boxwidget'

    var Default = {
        animationSpeed: 500,
        collapseTrigger: '[data-widget="collapse"]',
        removeTrigger: '[data-widget="remove"]',
        collapseIcon: 'fa-minus',
        expandIcon: 'fa-plus',
        removeIcon: 'fa-times'
    }

    var Selector = {
        data: '.box',
        collapsed: '.collapsed-box',
        body: '.box-body',
        footer: '.box-footer',
        tools: '.box-tools'
    }

    var ClassName = {
        collapsed: 'collapsed-box'
    }

    var Event = {
        collapsed: 'collapsed.boxwidget',
        expanded: 'expanded.boxwidget',
        removed: 'removed.boxwidget'
    }

    // BoxWidget Class Definition
    var BoxWidget = function (element, options) {
        this.element = element
        this.options = options

        this._setUpListeners()
    }

    BoxWidget.prototype.toggle = function () {
        var isOpen = !$(this.element).is(Selector.collapsed)

        if (isOpen) {
            this.collapse()
        } else {
            this.expand()
        }
    }

    BoxWidget.prototype.expand = function () {
        var expandedEvent = $.Event(Event.expanded)
        var collapseIcon = this.options.collapseIcon
        var expandIcon = this.options.expandIcon

        $(this.element).removeClass(ClassName.collapsed)

        $(this.element)
            .find(Selector.tools)
            .find('.' + expandIcon)
            .removeClass(expandIcon)
            .addClass(collapseIcon)

        $(this.element).find(Selector.body + ', ' + Selector.footer)
            .slideDown(this.options.animationSpeed, function () {
                $(this.element).trigger(expandedEvent)
            }.bind(this))
    }

    BoxWidget.prototype.collapse = function () {
        var collapsedEvent = $.Event(Event.collapsed)
        var collapseIcon = this.options.collapseIcon
        var expandIcon = this.options.expandIcon

        $(this.element)
            .find(Selector.tools)
            .find('.' + collapseIcon)
            .removeClass(collapseIcon)
            .addClass(expandIcon)

        $(this.element).find(Selector.body + ', ' + Selector.footer)
            .slideUp(this.options.animationSpeed, function () {
                $(this.element).addClass(ClassName.collapsed)
                $(this.element).trigger(collapsedEvent)
            }.bind(this))
    }

    BoxWidget.prototype.remove = function () {
        var removedEvent = $.Event(Event.removed)

        $(this.element).slideUp(this.options.animationSpeed, function () {
            $(this.element).trigger(removedEvent)
            $(this.element).remove()
        }.bind(this))
    }

    // Private

    BoxWidget.prototype._setUpListeners = function () {
        var that = this

        $(this.element).on('click', this.options.collapseTrigger, function (event) {
            if (event) event.preventDefault()
            that.toggle()
        })

        $(this.element).on('click', this.options.removeTrigger, function (event) {
            if (event) event.preventDefault()
            that.remove()
        })
    }

    // Plugin Definition
    function Plugin(option) {
        return this.each(function () {
            var $this = $(this)
            var data = $this.data(DataKey)

            if (!data) {
                var options = $.extend({}, Default, $this.data(), typeof option === 'object' && option)
                $this.data(DataKey, (data = new BoxWidget($this, options)))
            }

            if (typeof option == 'string') {
                if (typeof data[option] == 'undefined') {
                    throw new Error('No method named ' + option)
                }
                data[option]()
            }
        })
    }

    var old = $.fn.boxWidget

    $.fn.boxWidget = Plugin
    $.fn.boxWidget.Constructor = BoxWidget

    // No Conflict Mode
    $.fn.boxWidget.noConflict = function () {
        $.fn.boxWidget = old
        return this
    }

    // BoxWidget Data API
    $(window).on('load', function () {
        $(Selector.data).each(function () {
            Plugin.call($(this))
        })
    })

}(jQuery) // End of use strict


    /* TodoList()
     * Converts a list into a todoList.
     *
     * @Usage: $('.my-list').todoList(options)
     *         or add [data-widget="todo-list"] to the ul element
     *         Pass any option as data-option="value"
     */
+ function ($) {
    'use strict'

    var DataKey = 'aries.todolist'

    var Default = {
        iCheck: false,
        onCheck: function () {
        },
        onUnCheck: function () {
        }
    }

    var Selector = {
        data: '[data-widget="todo-list"]'
    }

    var ClassName = {
        done: 'done'
    }

    // TodoList Class Definition
    var TodoList = function (element, options) {
        this.element = element
        this.options = options

        this._setUpListeners()
    }

    TodoList.prototype.toggle = function (item) {
        item.parents(Selector.li).first().toggleClass(ClassName.done)
        if (!item.prop('checked')) {
            this.unCheck(item)
            return
        }

        this.check(item)
    }

    TodoList.prototype.check = function (item) {
        this.options.onCheck.call(item)
    }

    TodoList.prototype.unCheck = function (item) {
        this.options.onUnCheck.call(item)
    }

    // Private

    TodoList.prototype._setUpListeners = function () {
        var that = this
        $(this.element).on('change ifChanged', 'input:checkbox', function () {
            that.toggle($(this))
        })
    }

    // Plugin Definition
    function Plugin(option) {
        return this.each(function () {
            var $this = $(this)
            var data = $this.data(DataKey)

            if (!data) {
                var options = $.extend({}, Default, $this.data(), typeof option === 'object' && option)
                $this.data(DataKey, (data = new TodoList($this, options)))
            }

            if (typeof data == 'string') {
                if (typeof data[option] == 'undefined') {
                    throw new Error('No method named ' + option)
                }
                data[option]()
            }
        })
    }

    var old = $.fn.todoList

    $.fn.todoList = Plugin
    $.fn.todoList.Constructor = TodoList

    // No Conflict Mode
    $.fn.todoList.noConflict = function () {
        $.fn.todoList = old
        return this
    }

    // TodoList Data API
    $(window).on('load', function () {
        $(Selector.data).each(function () {
            Plugin.call($(this))
        })
    })

}(jQuery) // End of use strict


    /* DirectChat()
     * Toggles the state of the control sidebar
     *
     * @Usage: $('#my-chat-box').directChat()
     *         or add [data-widget="direct-chat"] to the trigger
     */
+ function ($) {
    'use strict'

    var DataKey = 'aries.directchat'

    var Selector = {
        data: '[data-widget="chat-pane-toggle"]',
        box: '.direct-chat'
    }

    var ClassName = {
        open: 'direct-chat-contacts-open'
    }

    // DirectChat Class Definition
    var DirectChat = function (element) {
        this.element = element
    }

    DirectChat.prototype.toggle = function ($trigger) {
        $trigger.parents(Selector.box).first().toggleClass(ClassName.open)
    }

    // Plugin Definition
    function Plugin(option) {
        return this.each(function () {
            var $this = $(this)
            var data = $this.data(DataKey)

            if (!data) {
                $this.data(DataKey, (data = new DirectChat($this)))
            }

            if (typeof option == 'string') data.toggle($this)
        })
    }

    var old = $.fn.directChat

    $.fn.directChat = Plugin
    $.fn.directChat.Constructor = DirectChat

    // No Conflict Mode
    $.fn.directChat.noConflict = function () {
        $.fn.directChat = old
        return this
    }

    // DirectChat Data API
    $(document).on('click', Selector.data, function (event) {
        if (event) event.preventDefault()
        Plugin.call($(this), 'toggle')
    })

    // Slim scrolling

    $('.inner-content-div').slimScroll({
        height: 'auto'
    });


    $(".search-box a, .search-box .app-search .srh-btn").on('click', function () {
        $(".app-search").toggle(200);
    });


    // Close
    //
    $(document).on('click', '.box-btn-close', function () {
        $(this).parents('.box').fadeOut(600, function () {
            if ($(this).parent().children().length == 1) {
                $(this).parent().remove();
            }
            else {
                $(this).remove();
            }
        });
    });


    // Slide up/down
    //
    $(document).on('click', '.box-btn-slide', function () {
        $(this).toggleClass('rotate-180').parents('.box').find('.box-content').slideToggle();
    });


    // Maximize
    //
    $(document).on('click', '.box-btn-maximize', function () {
        $(this).parents('.box').toggleClass('box-maximize').removeClass('box-fullscreen');
    });


    // Fullscreen
    //
    $(document).on('click', '.box-btn-fullscreen', function () {
        $(this).parents('.box').toggleClass('box-fullscreen').removeClass('box-maximize');
    });


    // Disable demonstrative links!
    //
    $(document).on('click', 'a[href="#"]', function (e) {
        e.preventDefault();
    });


    // Upload
    //
    $(document).on('click', '.file-browser', function () {
        var $browser = $(this);
        if ($browser.hasClass('form-control')) {
            setTimeout(function () {
                $browser.closest('.file-group').find('[type="file"]').trigger('click');
            }, 300);
        }
        else {
            var file = $browser.closest('.file-group').find('[type="file"]');
            file.on('click', function (e) {
                e.stopPropagation();
            });
            file.trigger('click');
        }
    });

    // Event to change file name after file selection
    $(document).on('change', '.file-group [type="file"]', function () {
        var input = $(this)[0];
        var len = input.files.length;
        var filename = '';

        for (var i = 0; i < len; ++i) {
            filename += input.files.item(i).name + ', ';
        }
        filename = filename.substr(0, filename.length - 2);
        $(this).closest('.file-group').find('.file-value').val(filename).text(filename).focus();
    });

    // Update file name for bootstrap custom file upload
    $(document).on('change', '.custom-file-input', function () {
        var filename = $(this).val().split('\\').pop();
        $(this).next('.custom-file-control').attr('data-input-value', filename);
    });
    $('.custom-file-control:not([data-input-value])').attr('data-input-value', 'Choose file...');

}(jQuery) // End of use strict
accessid = ''
accesskey = ''
host = ''
policyBase64 = ''
signature = ''
callbackbody = ''
filename = ''
key = ''
expire = 0
g_object_name = ''
g_object_name_type = ''
now = timestamp = Date.parse(new Date()) / 1000;

function send_request() {
    var xmlhttp = null;
    if (window.XMLHttpRequest) {
        xmlhttp = new XMLHttpRequest();
    }
    else if (window.ActiveXObject) {
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }

    if (xmlhttp != null) {
        // serverUrl是 用户获取 '签名和Policy' 等信息的应用服务器的URL，请将下面的IP和Port配置为您自己的真实信息。
        serverUrl = '/admin/oss_token'

        xmlhttp.open("GET", serverUrl, false);
        xmlhttp.send(null);
        return xmlhttp.responseText
    }
    else {
        alert("Your browser does not support XMLHTTP.");
    }
};

function check_object_radio() {
    var tt = document.getElementsByName('myradio');
    for (var i = 0; i < tt.length; i++) {
        if (tt[i].checked) {
            g_object_name_type = tt[i].value;
            break;
        }
    }
}

function get_signature() {
    // 可以判断当前expire是否超过了当前时间， 如果超过了当前时间， 就重新取一下，3s 作为缓冲。
    now = timestamp = Date.parse(new Date()) / 1000;
    if (expire < now + 3) {
        body = send_request()
        var obj = eval("(" + body + ")");
        host = obj['host']
        policyBase64 = obj['policy']
        accessid = obj['accessid']
        signature = obj['signature']
        expire = parseInt(obj['expire'])
        callbackbody = obj['callback']
        key = obj['dir']
        return true;
    }
    return false;
};

function random_string(len) {
    len = len || 32;
    var chars = 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678';
    var maxPos = chars.length;
    var pwd = '';
    for (i = 0; i < len; i++) {
        pwd += chars.charAt(Math.floor(Math.random() * maxPos));
    }
    return pwd;
}

function get_suffix(filename) {
    pos = filename.lastIndexOf('.')
    suffix = ''
    if (pos != -1) {
        suffix = filename.substring(pos)
    }
    return suffix;
}

function calculate_object_name(filename) {
    if (g_object_name_type == 'local_name') {
        g_object_name += "${filename}"
    }
    else if (g_object_name_type == 'random_name') {
        suffix = get_suffix(filename)
        g_object_name = key + random_string(10) + suffix
    }
    return ''
}

function get_uploaded_object_name(filename) {
    if (g_object_name_type == 'local_name') {
        tmp_name = g_object_name
        tmp_name = tmp_name.replace("${filename}", filename);
        return tmp_name
    }
    else if (g_object_name_type == 'random_name') {
        return g_object_name
    }
}

function set_upload_param(up, filename, ret) {
    if (ret == false) {
        ret = get_signature()
    }
    g_object_name = key;
    if (filename != '') {
        suffix = get_suffix(filename)
        calculate_object_name(filename)
    }
    new_multipart_params = {
        'key': g_object_name,
        'policy': policyBase64,
        'OSSAccessKeyId': accessid,
        'success_action_status': '200', //让服务端返回200,不然，默认会返回204
        'callback': callbackbody,
        'signature': signature,
    };

    up.setOption({
        'url': host,
        'multipart_params': new_multipart_params
    });

    up.start();
}

//plupload
function initPlupload(element, maxFiles = 1, extData) {
    var uploader = new plupload.Uploader({
        runtimes: 'html5,flash,silverlight,html4',// 上传模式，依次退化
        browse_button: element,// 上传选择的点选按钮，必需
        //container: document.getElementById(element),
        //multi_selection: false,
        flash_swf_url: '../../components/plupload/js/Moxie.swf',
        silverlight_xap_url: '../../components/plupload/js/Moxie.xap',
        multipart_params: extData,
        url: '/admin/upload',
        auto_start: true, // 选择文件后自动上传，若关闭需要自己绑定事件触发上传
        filters: {
            mime_types: [ //只允许上传图片和zip文件
                {title: "Image files", extensions: "jpg,gif,png,bmp"},
                {title: "Zip files", extensions: "zip,rar"}
            ],
            max_file_size: '10mb', //最大只能上传10mb的文件
            prevent_duplicates: true //不允许选取重复文件
        },
        init: {
            'FilesAdded': function (up, files) {
                plupload.each(files, function (file) {
// 文件添加进队列后,处理相关的事情 

                });
            },
            'BeforeUpload': function (up, file) {
// 每个文件上传前,处理相关的事情 
            },
            'UploadProgress': function (up, file) {
// 每个文件上传时,处理相关的事情 
            },
            'UploadComplete': function () {
//队列文件处理完毕后,处理相关的事情 

            },
            'FileUploaded': function (up, file, info) {
                if (info.status == 200) {
                    var response = eval("(" + info.response + ")");
                    showAllFiles(element,response.file_name)
                }
                else {
                    toastr.error(info.response);
                }
            },
            Error: function (up, err) {
                if (err.code == -600) {
                    toastr.error("选择的文件太大了");
                }
                else if (err.code == -601) {
                    toastr.error("选择的文件后缀不对");
                }
                else if (err.code == -602) {
                    toastr.error("这个文件已经上传过一遍了");
                }
                else {
                    toastr.error(err.response);
                }
            }
        }
    });
    uploader.init();
}
//plupload清空展示的文件
function clearAllPreviousFiles(element) {
    var previous = document.getElementById(element).previousSibling;
    if (previous) {
        previous.parentNode.removeChild(previous)
        clearAllPreviousFiles(element)
    }else {
        return
    }
}
//plupload展示列表的文件
function showAllFiles(element,newFile) {
    var arr = []
    var formInput = document.getElementById(element).nextElementSibling;
    var oldFile = formInput.value
    if (oldFile) {
         arr = oldFile.split(',');//转数组
    }
    if (newFile){
        arr.push(newFile)//添加新上传的文件
    }
    formInput.value = arr.join(',');//转字符
    clearAllPreviousFiles(element) //清空所有已添加的数据
    arr.forEach(function (v) {
        var img = document.createElement('div');
        img.className = 'col-sm-2 pluploadshow';
        img.setAttribute('file_data', v);
        img.style.backgroundImage = "url(" +v + ")";
        var remove = document.createElement('div');
        remove.className = 'remove-btn';
        var icon = document.createElement('i');
        icon.className = 'fa fa-times'
        remove.appendChild(icon);
        img.appendChild(remove);
        document.getElementById(element).parentNode.insertBefore(img, document.getElementById(element));
                //plupload 移除文件
        $(remove).on('click',function(){
            var removefile = $(this).parent().attr('file_data')
            var index = arr.indexOf(removefile);
            if (index > -1) {
                arr.splice(index, 1);
            }
            formInput.value =arr.join(",");
            showAllFiles(element)
        })
    });
}

//上传到本地
function initImageUpload(element, maxFiles = 1, extData, formInput, info) {
    var myDropzone = new Dropzone(element, {
        url: "/admin/upload",//上传文件的地址，
        maxFiles: maxFiles,//最多上传几个图片
        params: extData,
        maxFilesize: 5,//图片的大小，单位是M
        addRemoveLinks: false,//是否有删除图片的功能
        acceptedFiles: "image/*",//支持的格式
        paramName: 'file',//上传的FILE名称，即服务端可以通过此来获取上传的图片，如$_FILES['dropimage']
        dictDefaultMessage: "将文件拖至此处或点击上传....",
        dictInvalidFileType: "格式错误,请上传图片...",
        dictResponseError: "服务器连接失败...",
        dictMaxFilesExceeded: "不能上传这么多...",
        dictRemoveFile: "移除文件",
        previewTemplate: "<div class=\"dz-preview dz-file-preview\">\n  " +
        "<div class=\"dz-image\">\n    " +
        "<img data-dz-thumbnail />\n " +
        "</div>\n  " +
        "<div class=\"dz-details\">\n    " +
        "<div class=\"dz-filename\"><span data-dz-name></span></div>\n " +
        "<a class=\"dz-delete\" onclick='removeFile(this)' data-dz-remove><i class='fa fa-close'></i>删除</a>\n " +
        "</div>\n  " +
        "<div class=\"dz-progress\"><span class=\"dz-upload\" data-dz-uploadprogress></span></div>\n " +
        " <div class=\"dz-success-mark\"><span></span></div>\n " +
        " <div class=\"dz-error-mark\"><span></span></div>\n " +
        " <div class=\"dz-error-message\"><span data-dz-errormessage></span></div>\n" +
        "</div>",
    });
    if (info) {
        initImageShow(myDropzone, info)
    }
    myDropzone.on("success", function (file, response) {
        myDropzone.removeFile(file);
        initImageShow(myDropzone, response.file_name)
        if (response.code == 1) {
            var arr = []
            if (formInput.val()) {
                var arr = formInput.val().split(',');//转数组
            }
            arr.push(response.file_name)//添加新上传的文件
            formInput.val(arr.join(','));//转字符
        } else {
            toastr.error(response.msg);
        }
    });
    myDropzone.on("removedfile", function (file) {
        var arr = formInput.val().split(',');
        var index = arr.indexOf(file_to_path(file.name));
        if (index > -1) {
            arr.splice(index, 1);
        }
        formInput.val(arr.join(","));
    });
    return myDropzone
}
// 编辑时显示已有数据
function initImageShow(dz, info) {
    if (info == '' || !info) return false;
    var info_array = info.split(",");
    for (var i in info_array) {
        var hidefileval_str = info_array[i];
        var hidefileval_arr = hidefileval_str.split("/");
        var mockfile_object = {name: hidefileval_arr[hidefileval_arr.length - 1], accepted: true}
        dz.emit('addedfile', mockfile_object);
        dz.emit('thumbnail', mockfile_object, hidefileval_str);
        dz.emit('processing', mockfile_object);
        dz.emit('complete', mockfile_object);
        dz.files.push(mockfile_object);
        mockfile_object = null;
    }
}
//彻底删除文件
function removeFile(obj) {
    var file_name = $(obj).prev()[0].innerText
    $.ajax({
        type: "POST",//方法类型
        dataType: "json",//预期服务器返回的数据类型
        url: "/admin/del_file",
        data: {
            csrf_token: extraData['csrf_token'],
            "file_name": file_name
        },
        success: function (result) {
            if (result.code == 1) {
                toastr.success(result.msg);
            } else {
                toastr.error(result.msg);
            }
            ;
        },
        error: function () {
            toastr.error("服务器异常，请稍后重试！");
        }
    });
}
//根据文件名称获取路径
function file_to_path(file_name) {
    return "/static/uploads/" + file_name.substring(0, 8) + "/" + file_name;
}
//删除方法
function deleteFun(obj) {
    //禁用提交按钮，避免重复提交
    obj.disabled = true;
    var url = $(obj).attr('url');
    var id = $(obj).attr('id');
    var csrftoken = $(obj).attr('csrftoken');
    swal({
        title: "确定删除?",
        text: "删除后将无法恢复!",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#DD6B55",
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        closeOnConfirm: false
    }, function () {
        $.ajax({
            type: "DELETE",//方法类型
            dataType: "json",//预期服务器返回的数据类型
            url: url,//url
            headers: {"X-CSRFToken": csrftoken},
            data: {"id": id},
            success: function (result) {
                if (result.code == 1) {
                    toastr.success(result.msg);
                    setTimeout(function () {
                        window.location.reload();
                    }, 1000);
                } else {
                    toastr.error(result.msg);
                    obj.disabled = false;
                }
                ;
            },
            error: function () {
                toastr.error("服务器异常，请稍后重试！");
            }
        });
    })
}

function updateFun(obj) {
    //禁用提交按钮，避免重复提交
    obj.disabled = true;
    var url = $(obj).attr('url');
    var formId = $(obj).attr('formId');
    var form = $('#' + formId)
    $.ajax({
        type: "PUT",//方法类型
        dataType: "json",//预期服务器返回的数据类型
        url: url,//url
        data: form.serialize(),
        success: function (result) {
            if (result.code == 1) {
                toastr.success(result.msg);
                setTimeout(function () {
                    window.location.reload();
                }, 1000);
            } else {
                toastr.error(result.msg);
                obj.disabled = false;
            }
            ;
        },
        error: function () {
            toastr.error("服务器异常，请稍后重试！");
        }
    });

}

function addFun(obj) {
    //禁用提交按钮，避免重复提交
    obj.disabled = true;
    var url = $(obj).attr('url');
    var formId = $(obj).attr('formId');
    var form = $('#' + formId)
    $.ajax({
        //几个参数需要注意一下
        type: "POST",//方法类型
        dataType: "json",//预期服务器返回的数据类型
        url: url,//url
        data: form.serialize(),
        success: function (result) {
            if (result.code == 1) {
                toastr.success(result.msg);
                setTimeout(function () {
                    window.location.reload();
                }, 1000);
            } else {
                toastr.error(result.msg);
                obj.disabled = false;
            }
            ;
        },
        error: function () {
            toastr.error("服务器异常，请稍后重试！");
        }
    });

}

function initEditor(ctrlName, extraData, defaultValue) {
    var E = window.wangEditor
    var editor = new E(ctrlName)
    editor.customConfig.menus = [
	 		    'head',  // 标题
			    'bold' /** 粗体*/, 'fontSize' /** 字号 */, 'fontName' /** 字体 */,'italic' /** 斜体 */,
	 		    'underline',  // 下划线
			    'strikeThrough',  // 删除线
			    'foreColor',  // 文字颜色
			    'backColor',  // 背景颜色
			    'link',  // 插入链接
			    'list',  // 列表
			    'justify',  // 对齐方式
			    'quote',  // 引用
	 		   // 'emoticon',  // 表情   打开后支持表情功能
			    'image',  // 插入图片
			    'table',  // 表格
			    'video',  // 插入视频
//	 		    'code',  // 插入代码
			    'undo',  // 撤销
			    'redo'  // 重复
	                         ]
    editor.customConfig.onchange = function (html) {
        // 监控变化，同步更新到 textarea
        $(ctrlName).next().val(html)
    }
    // 自定义上传图片事件
    editor.customConfig.customUploadImg = function (files, insert) {
        files.forEach(function (file) {
            const data = new FormData();
            data.append('file', file);
            Object.keys(extraData).forEach(function (key) {
                data.append(key, extraData[key]);
            });
            $.ajax({
                url: '/admin/upload',
                type: 'POST',
                data: data,
                dataType: 'json',
                processData: false,
                contentType: false,
                success: function (data) {
                    if (data.file_name) {
                        // 上传代码返回结果之后，将图片插入到编辑器中
                        insert(data.file_name);
                    } else {
                        toastr.error(data.msg);
                    }
                }
            });
        })
    }
    editor.create()
    editor.txt.html(defaultValue)
}
function strToArr(str) {
    if (str) {
        return str.split(",");
    }
}

//全选和反选

$("#select-all").change(
    function () {
        if ($(this).is(":checked")) {
            $("[name='selected']").prop("checked", true);
        } else {
            $("[name='selected']").prop("checked", false);
        }
    }
)

//获取所有选中checkbox的值
function checkedValue() {
    var arr = new Array();
    $("input:checkbox[name='selected']:checked").each(function (i) {
        arr.push($(this).attr('id'))
    });
    return arr.join(',');
}
function showicon(obj) {
        icon = $(obj).siblings().children().children()
        icon.removeClass()
        icon.addClass("fa")
        icon.addClass(obj.value)
    }